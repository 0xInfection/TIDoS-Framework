import re
import logging
import Resolver


class SpfRecord(object):

    def __init__(self, domain):
        self.version = None
        self.record = None
        self.mechanisms = None
        self.all_string = None
        self.domain = domain
        self.recursion_depth = 0

    def __str__(self):
        return self.record

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def get_redirected_record(self):
        if self.recursion_depth >= 10:
            return SpfRecord(self.get_redirect_domain())
        else:
            redirect_domain = self.get_redirect_domain()
            if redirect_domain is not None:
                redirect_record = SpfRecord.from_domain(redirect_domain)
                redirect_record.recursion_depth = self.recursion_depth + 1
                return redirect_record

    def get_redirect_domain(self):
        redirect_domain = None
        if self.mechanisms is not None:
            for mechanism in self.mechanisms:
                redirect_mechanism = re.match('redirect=(.*)', mechanism)
                if redirect_mechanism is not None:
                    redirect_domain = redirect_mechanism.group(1)
            return redirect_domain

    def get_include_domains(self):
        include_domains = []
        if self.mechanisms is not None:
            for mechanism in self.mechanisms:
                include_mechanism = re.match('include:(.*)', mechanism)
                if include_mechanism is not None:
                    include_domains.append(include_mechanism.group(1))
            return include_domains
        else:
            return []

    def get_include_records(self):
        if self.recursion_depth >= 10:
            return {}
        else:
            include_domains = self.get_include_domains()
            include_records = {}
            for domain in include_domains:
                try:
                    include_records[domain] = SpfRecord.from_domain(domain)
                    include_records[domain].recursion_depth = self.recursion_depth + 1
                except IOError as e:
                    logging.exception(e)
                    include_records[domain] = None
            return include_records

    def _is_all_mechanism_strong(self):
        strong_spf_all_string = True
        if self.all_string is not None:
            if not (self.all_string == "~all" or self.all_string == "-all"):
                strong_spf_all_string = False
        else:
            strong_spf_all_string = False
        return strong_spf_all_string

    def _is_redirect_mechanism_strong(self):
        redirect_domain = self.get_redirect_domain()

        if redirect_domain is not None:
            redirect_mechanism = SpfRecord.from_domain(redirect_domain)

            if redirect_mechanism is not None:
                return redirect_mechanism.is_record_strong()
            else:
                return False
        else:
            return False

    def _are_include_mechanisms_strong(self):
        include_records = self.get_include_records()
        for record in include_records:
            if include_records[record] is not None and include_records[record].is_record_strong():
                return True
        return False

    def is_record_strong(self):
        strong_spf_record = self._is_all_mechanism_strong()
        if strong_spf_record is False:

            redirect_strength = self._is_redirect_mechanism_strong()
            include_strength = self._are_include_mechanisms_strong()

            strong_spf_record = False

            if redirect_strength is True:
                strong_spf_record = True

            if include_strength is True:
                strong_spf_record = True
        return strong_spf_record

    @staticmethod
    def from_spf_string(spf_string, domain):
        if spf_string is not None:
            spf_record = SpfRecord(domain)
            spf_record.record = spf_string
            spf_record.mechanisms = _extract_mechanisms(spf_string)
            spf_record.version = _extract_version(spf_string)
            spf_record.all_string = _extract_all_mechanism(spf_record.mechanisms)
            return spf_record
        else:
            return SpfRecord(domain)

    @staticmethod
    def from_domain(domain):
        spf_string = get_spf_string_for_domain(domain)
        if spf_string is not None:
            return SpfRecord.from_spf_string(spf_string, domain)
        else:
            return SpfRecord(domain)


def _extract_version(spf_string):
    version_pattern = "^v=(spf.)"
    version_match = re.match(version_pattern, spf_string)
    if version_match is not None:
        return version_match.group(1)
    else:
        return None


def _extract_all_mechanism(mechanisms):
    all_mechanism = None
    for mechanism in mechanisms:
        if re.match(".all", mechanism):
            all_mechanism = mechanism
    return all_mechanism


def _find_unique_mechanisms(initial_mechanisms, redirected_mechanisms):
    return [x for x in redirected_mechanisms if x not in initial_mechanisms]


def _extract_mechanisms(spf_string):
    spf_mechanism_pattern = ("(?:((?:\+|-|~)?(?:a|mx|ptr|include"
                             "|ip4|ip6|exists|redirect|exp|all)"
                             "(?:(?::|=|/)?(?:\S*))?) ?)")
    spf_mechanisms = re.findall(spf_mechanism_pattern, spf_string)

    return spf_mechanisms


def _merge_txt_record_strings(txt_record):
    # SPF spec requires that TXT records containing multiple strings be cat'd together.
    string_pattern = re.compile('"([^"]*)"')
    txt_record_strings = string_pattern.findall(txt_record)
    return "".join(txt_record_strings)


def _match_spf_record(txt_record):
    clean_txt_record = _merge_txt_record_strings(txt_record)
    spf_pattern = re.compile('^(v=spf.*)')
    potential_spf_match = spf_pattern.match(str(clean_txt_record))
    return potential_spf_match


def _find_record_from_answers(txt_records):
    spf_record = None
    for record in txt_records:
        potential_match = _match_spf_record(record[2])
        if potential_match is not None:
            spf_record = potential_match.group(1)
    return spf_record


def get_spf_string_for_domain(domain):
    try:
        txt_records = Resolver.resolver().query(domain, query_type="TXT")
        return _find_record_from_answers(txt_records)
    except IOError as e:
        # This is returned usually as a NXDOMAIN, which is expected.
        return None

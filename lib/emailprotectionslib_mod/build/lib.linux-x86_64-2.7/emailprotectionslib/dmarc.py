import re
import logging
import Resolver
import tldextract


class DmarcRecord(object):

    def __init__(self, domain):
        self.domain = domain
        self.version = None
        self.policy = None
        self.pct = None
        self.rua = None
        self.ruf = None
        self.subdomain_policy = None
        self.dkim_alignment = None
        self.spf_alignment = None
        self.record = None

    def __str__(self):
        return self.record

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def _store_tag_data(self, tag_name, tag_value):
        if tag_name == "v":
            self.version = tag_value
        elif tag_name == "p":
            self.policy = tag_value
        elif tag_name == "pct":
            self.pct = tag_value
        elif tag_name == "rua":
            self.rua = tag_value
        elif tag_name == "ruf":
            self.ruf = tag_value
        elif tag_name == "sp":
            self.subdomain_policy = tag_value
        elif tag_name == "adkim":
            self.dkim_alignment = tag_value
        elif tag_name == "aspf":
            self.spf_alignment = tag_value

    def process_tags(self, dmarc_string):
        TAG_NAME, TAG_VALUE = (0, 1)
        tags = _extract_tags(dmarc_string)
        for tag in tags:
            self._store_tag_data(tag[TAG_NAME], tag[TAG_VALUE])

    def is_record_strong(self):
        record_strong = False
        if self.policy is not None and (self.policy == "reject" or self.policy == "quarantine"):
            record_strong = True

        if not record_strong:
            try:
                record_strong = self.is_org_domain_strong()
            except OrgDomainException:
                record_strong = False

        return record_strong

    def is_subdomain_policy_strong(self):
        if self.subdomain_policy is not None:
            return self.subdomain_policy == "reject" or self.subdomain_policy == "quarantine"

    def is_org_domain_strong(self):
        org_record = self.get_org_record()
        subdomain_policy_strong = org_record.is_subdomain_policy_strong()
        if subdomain_policy_strong is not None:
            return subdomain_policy_strong
        else:
            return org_record.is_record_strong()

    def get_org_record(self):
        org_domain = self.get_org_domain()
        if org_domain == self.domain:
            raise OrgDomainException
        else:
            return DmarcRecord.from_domain(org_domain)

    def get_org_domain(self):
        try:
            domain_parts = tldextract.extract(self.domain)
            return "%(domain)s.%(tld)s" % {'domain': domain_parts.domain, 'tld': domain_parts.suffix}
        except TypeError:
            return None

    @staticmethod
    def from_dmarc_string(dmarc_string, domain):
        if dmarc_string is not None:
            dmarc_record = DmarcRecord(domain)
            dmarc_record.record = dmarc_string
            dmarc_record.process_tags(dmarc_string)
            return dmarc_record
        else:
            return DmarcRecord(domain)

    @staticmethod
    def from_domain(domain):
        dmarc_string = get_dmarc_string_for_domain(domain)
        if dmarc_string is not None:
            return DmarcRecord.from_dmarc_string(dmarc_string, domain)
        else:
            return DmarcRecord(domain)


def _extract_tags(dmarc_record):
    dmarc_pattern = "(\w+)=(.*?)(?:; ?|$)"
    return re.findall(dmarc_pattern, dmarc_record)


def _merge_txt_record_strings(txt_record):
    # DMARC spec requires that TXT records containing multiple strings be cat'd together.
    string_pattern = re.compile('"([^"]*)"')
    txt_record_strings = string_pattern.findall(txt_record)
    return "".join(txt_record_strings)


def _match_dmarc_record(txt_record):
    merged_txt_record = _merge_txt_record_strings(txt_record)
    dmarc_pattern = re.compile('^(v=DMARC.*)')
    potential_dmarc_match = dmarc_pattern.match(str(merged_txt_record))
    return potential_dmarc_match


def _find_record_from_answers(txt_records):
    dmarc_record = None
    for record in txt_records:
        potential_match = _match_dmarc_record(record[2])
        if potential_match is not None:
            dmarc_record = potential_match.group(1)
    return dmarc_record


def get_dmarc_string_for_domain(domain):
    try:
        txt_records = Resolver.resolver().query("_dmarc." + domain, query_type="TXT")
        return _find_record_from_answers(txt_records)
    except IOError:
        # This is returned usually as a NXDOMAIN, which is expected.
        return None
    except TypeError as error:
        logging.exception(error)
        return None


class OrgDomainException(Exception):
    pass

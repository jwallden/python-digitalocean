# -*- coding: utf-8 -*-
import requests
from .Record import Record
from .baseapi import BaseAPI

class Domain(BaseAPI):
    def __init__(self, *args, **kwargs):
        self.name = None
        self.ttl = None
        self.zone_file = None
        self.ip_address = None

        super(Domain, self).__init__(*args, **kwargs)

    @classmethod
    def get_object(cls, api_token, domain_name):
        """
            Class method that will return a Domain object by ID.
        """
        domain = cls(token=api_token, name=domain_name)
        domain.load()
        return domain

    def load(self):
        # URL https://api.digitalocean.com/v2/domains
        domains = self.get_data("domains/%s" % self.name)

        for attr in list(domains.keys()):
            setattr(self,attr,droplet[attr])

    def destroy(self):
        """
            Destroy the domain by name
        """
        # URL https://api.digitalocean.com/v2/domains/[NAME]
        return self.get_data(
            "domains/%s" % self.name,
            type="DELETE"
        )

    def create_new_domain_record(self, *args, **kwargs):
        """
            Create new domain record.
            https://developers.digitalocean.com/#create-a-new-domain-record

            Args:

            @type  The record type (A, MX, CNAME, etc).
            @name  The host name, alias, or service being defined by the record
            @data  Variable data depending on record type.

            Optional Args:

            @priority The priority of the host
            @port The port that the service is accessible on
            @weight The weight of records with the same priority
        """
        data = {
            "type": kwargs.get("type", None),
            "name": kwargs.get("name", None),
            "data": kwargs.get("data", None)
        }

        # Optional Args
        if kwargs.get("priority", None):
            data['priority'] = kwargs.get("priority", None)

        if kwargs.get("port", None):
            data['port'] = kwargs.get("port", None)

        if kwargs.get("weight", None):
            data['weight'] = kwargs.get("weight", None)

        return self.get_data(
            "domains/%s/records" % self.name,
            type="POST",
            params=data
        )

    def create(self):
        """
            Create new doamin
        """
        # URL https://api.digitalocean.com/v2/domains
        data = {
                "name": self.name,
                "ip_address": self.ip_address,
            }

        domain = self.get_data(
            "domains",
            type="POST",
            params=data
        )
        return domain

    def get_records(self):
        """
            Returns a list of Record objects
        """
        # URL https://api.digitalocean.com/v2/domains/[NAME]/records/
        records = []
        data = self.get_data(
            "domains/%s/records/" % self.name,
            type="GET",
        )

        for record_data in data['domain_records']:

            record = Record(**record_data)
            record.token = self.token
            records.append(record)

        return records

    def __str__(self):
        return "%s" % self.name
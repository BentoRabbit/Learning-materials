# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Clinicaltrial(models.Model):
    rank = models.IntegerField(db_column='Rank', blank=True, null=True)  # Field name made lowercase.
    trial_id = models.CharField(db_column='Trial ID', primary_key=True, max_length=45)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    title = models.CharField(db_column='Title', max_length=500, blank=True, null=True)  # Field name made lowercase.
    brief_title = models.CharField(db_column='Brief title', max_length=500, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    acronym = models.CharField(db_column='Acronym', max_length=500, blank=True, null=True)  # Field name made lowercase.
    abstract = models.CharField(db_column='Abstract', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    detailed_description = models.CharField(db_column='Detailed Description', max_length=1500, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    start_year = models.IntegerField(db_column='Start_Year', blank=True, null=True)  # Field name made lowercase.
    completion_year = models.IntegerField(db_column='Completion_Year', blank=True, null=True)  # Field name made lowercase.
    phase = models.CharField(db_column='Phase', max_length=45, blank=True, null=True)  # Field name made lowercase.
    conditions = models.CharField(db_column='Conditions', max_length=500, blank=True, null=True)  # Field name made lowercase.
    intervention = models.CharField(db_column='Intervention', max_length=500, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=30, blank=True, null=True)  # Field name made lowercase.
    registry = models.CharField(db_column='Registry', max_length=30, blank=True, null=True)  # Field name made lowercase.
    investigators_contacts = models.CharField(db_column='Investigators/Contacts', max_length=500, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sponsors_collaborators = models.CharField(db_column='Sponsors/Collaborators', max_length=500, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    grid_ids = models.CharField(db_column='GRID IDs', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    city_of_sponsor_collaborator = models.CharField(db_column='City of Sponsor/Collaborator', max_length=80, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    state_of_sponsor_collaborator = models.CharField(db_column='State of Sponsor/Collaborator', max_length=45, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    country_of_sponsor_collaborator = models.CharField(db_column='Country of Sponsor/Collaborator', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    collaborating_funders = models.CharField(db_column='Collaborating Funders', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    funder_group = models.CharField(db_column='Funder Group', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    funder_country = models.CharField(db_column='Funder Country', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_linkout = models.CharField(db_column='Source Linkout', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dimensions_url = models.CharField(db_column='Dimensions URL', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    for_anzsrc_categories = models.CharField(db_column='FOR (ANZSRC) Categories', max_length=500, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rcdc_categories = models.CharField(db_column='RCDC Categories', max_length=500, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    hrcs_hc_categories = models.CharField(db_column='HRCS HC Categories', max_length=500, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    hrcs_rac_categories = models.CharField(db_column='HRCS RAC Categories', max_length=500, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    icrp_cancer_types = models.CharField(db_column='ICRP Cancer Types', max_length=500, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    icrp_cso_categories = models.CharField(db_column='ICRP CSO Categories', max_length=500, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    city1 = models.CharField(db_column='City1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    city2 = models.CharField(db_column='City2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    state1 = models.CharField(db_column='State1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    state2 = models.CharField(db_column='State2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    country1 = models.CharField(db_column='Country1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    country2 = models.CharField(db_column='Country2', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'clinicaltrial'


class ForAnzsrcData(models.Model):
    no = models.CharField(db_column='No', primary_key=True, max_length=500)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'for_anzsrc_data'


class State(models.Model):
    state = models.CharField(primary_key=True, max_length=50)
    state_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'state'


class User(models.Model):
    username = models.CharField(primary_key=True, max_length=45)
    password = models.CharField(max_length=45)
    email = models.CharField(max_length=45, blank=True, null=True)
    phone = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'

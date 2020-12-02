import json, os, django

# sys.path.append('..')

os.environ["DJANGO_SETTINGS_MODULE"] = "Datamed_Dashboard_Django.settings"
django.setup()

from bdpm.models import CompositionType, Component, Composition

FILE = "../Ressources/bdpm_partial.json"
DETAILED_LOG = True


class ReportValues:
    name = ""
    total_added = 0
    existing_occurrences = 0

    def __init__(self, name):
        self.name = name

    def __str__(self):
        print_value = ""
        print_value += self.name+ " : \n"
        print_value +="Total added : "+str(self.total_added)+"\n"
        total_iterated = self.existing_occurrences + self.total_added
        print_value +="For a total of " + str(total_iterated) + " objects \n"
        return str(print_value)

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()


def detailed_log(msg):
    print("--- "+msg) if DETAILED_LOG else False


report_values=[]


def execution_report():
    print("##### EXECUTION REPORT #####")
    print(report_values)
    #print("Composition types : ")

    #print("--- Added to DB : "+str(report_values["total_added_compotypes"])+" lines")
    #print("--- " + str(report_values["total_already_present_compotypes_occurrences"]) + " occurences of composition types wheren't new")


"""
-Checks if object already exists in DB, based on passe ddjango model and identifier field (unique field)
-If it doesn't exist, creates it based on passe django model and all fields dictionary
-Gets id (whether new or old) and returns it
-All this while feeding log list for log report
    -> django_object : object from django project referring to matching DB table
    -> id_field_dict : dictionary containing 1 element defining unicity of the object :
        key = property name  value = property unique value
        !!! to check : could contain unicity by 2 or more values (**kwargs)
        Will be used to check if object already is in DB
    -> all_fields_dict : all fields to create object if necessary
    -> log_list : list containing log elements, based on ReportValues class
    -> log object name : name of log object, for verbose log purpose. Example : "Spécialité"
-DEPENDENCIES : detailed_log function and ReportValues class
"""
def check_and_create(
        django_object,
        id_field_dict,
        all_fields_dict,
        log_list,
        log_object_name,
):
    detailed_log(log_object_name + " : " + str(id_field_dict))

    # takes log_object list and checks if this
    if next((e for e in log_list if e.name == log_object_name), False):
        report_elem = next(e for e in log_list if e.name == log_object_name)
    else:
        log_list.append(ReportValues(log_object_name))
        report_elem = next(e for e in log_list if e.name == log_object_name)

    doesItemExist = django_object.objects.filter(**id_field_dict).exists()  # checks if compo type already exists
    if not doesItemExist:
        detailed_log(log_object_name + " does not exist. Saving to DB")
        item = django_object.objects.create(**all_fields_dict)
        item_id = item.id
        report_elem.total_added += 1
        detailed_log(log_object_name + " added to db under id " + str(item_id))
    else:
        item_id = django_object.objects.get(**id_field_dict).id
        detailed_log(log_object_name + " already exists under id " + str(item_id) + ", skipping.")
        report_elem.existing_occurrences += 1

    return item_id


detailed_log("Detailed log activated")
print("Loading file "+FILE)

with open(FILE, "r", encoding='utf8') as read_file:
    data = json.load(read_file)
    print(str(len(data))+" specialtys to be loaded in DB")

    for med in data :
        print("Loading : "+med["title"])

        detailed_log(str(len(med["composition"]))+" compositions to load, iterating :")
        for composition in med["composition"]:
            ##### Composition type object
            id_composition_type = check_and_create(
                django_object = CompositionType,
                id_field_dict = {"name" : composition["type"]},
                all_fields_dict = {"name" : composition["type"]},
                log_list= report_values,
                log_object_name="Composition types",
            )
            print("################")
            detailed_log(str(len(composition["components"].keys())) + "components to load, iterating :")
            ##### Components Objects : make a list of objects
            list_id_components = []
            for component, dosage in composition["components"].items():
                detailed_log("Found "+component)
                print(component)
                print(dosage)
                list_id_components.append(
                    check_and_create(
                        django_object=Component,
                        id_field_dict={"name": component},
                        all_fields_dict={"name": component},
                        log_list=report_values,
                        log_object_name="Components",
                    )
                )
            print("-------------")

            ### Composition object
            Composition.objects.create(
                components=,
                quantity = ,
                type = ,
                specialty =
            )




        # IAB
        detailed_log("Loading iab items")
        iab_items = (med["iab"])
        if iab_items:
            detailed_log(str(len(iab_items))+" iab items")
            for iab_item in iab_items:
                print(iab_item)
                abstract = (iab_item["abstract"])
                advice = (iab_item["advice"])
                reason = (iab_item["reason"])
                value = (iab_item["value"])

        else:
            detailed_log("no iab items")

execution_report()
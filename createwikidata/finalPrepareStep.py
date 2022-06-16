import pandas as pd
import pywikibot

pywikibot.config.put_throttle = 0

site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()


def create_item(site, label_dict, des_dict):
    new_item = pywikibot.ItemPage(site)
    new_item.editLabels(labels=label_dict, summary="Setting labels")
    new_item.editDescriptions(des_dict, summary="Setting descriptions")
    # Add description here or in another function
    print(new_item.getID())
    return new_item.getID()


def set_claim(qnum, prop, obj):
    item = pywikibot.ItemPage(repo, qnum)
    claim = pywikibot.Claim(repo, prop)  # Adding located in the administrative territorial entity (P131)
    target = pywikibot.ItemPage(repo, obj)  # Connecting P131 with Cambridge (Q350), who is a Q-id.
    claim.setTarget(target)  # Set the target value in the local object.
    item.addClaim(claim, summary=u'Adding claim to ' + qnum)  # Inserting value with summary to Q210194


def set_claim_external_id(qnum, prop, eid):
    item = pywikibot.ItemPage(repo, qnum)
    claim = pywikibot.Claim(repo, prop)
    claim.setTarget(eid)  # Set the target value in the local object.
    item.addClaim(claim, summary=u'Adding claim to ' + qnum)  # Inserting value with summary to Q210194


def set_claim_item_identifier(qnum, prop, obj, qp, qo):
    item = pywikibot.ItemPage(repo, qnum)
    claim = pywikibot.Claim(repo, prop)  # Adding located in the administrative territorial entity (P131)
    target = pywikibot.ItemPage(repo, obj)  # Connecting P131 with Cambridge (Q350), who is a Q-id.
    claim.setTarget(target)  # Set the target value in the local object.
    item.addClaim(claim, summary=u'Adding claim to ' + qnum)  # Inserting value with summary to Q210194
    qualifier = pywikibot.Claim(repo, qp)
    target = pywikibot.ItemPage(repo, qo)
    qualifier.setTarget(target)
    claim.addQualifier(qualifier, summary=u'Adding a qualifier.')


def set_claim_url_itentifier(qnum, prop, obj, qp, qo):
    item = pywikibot.ItemPage(repo, qnum)
    claim = pywikibot.Claim(repo, prop)
    claim.setTarget(obj)
    item.addClaim(claim)
    qualifier = pywikibot.Claim(repo, qp)
    target = pywikibot.ItemPage(repo, qo)
    qualifier.setTarget(target)
    claim.addQualifier(qualifier, summary=u'Adding a qualifier.')


def check_pro_in_sub(qnum, prop, r, obj=0):
    item = pywikibot.ItemPage(repo, qnum)
    claims = item.get()["claims"]
    if (prop == "P106") and (obj == 'Q1240569'):
        if prop in claims:
            val = 0
            for claim in claims[prop]:
                target = claim.getTarget()
                objid = target.id
                if objid == 'Q1240569':
                    val += 1
            if val == 0:
                set_claim_item_identifier(qnum, "P106", 'Q1240569', "P1027", 'Q913861')
        else:
            set_claim_item_identifier(qnum, "P106", 'Q1240569', "P1027", 'Q913861')
    if prop == "P244":
        if prop not in claims:
            set_claim_external_id(qnum, prop, r["LCnum"])
    elif prop == "P69":
        if prop in claims:
            val = 0
            for claim in claims[prop]:
                target = claim.getTarget()
                objid = target.id
                if objid == r["SchoolQnum"]:
                    val += 1
            if val == 0:
                if pd.isnull(r["DegreeQnum"]):
                    set_claim(qnum, "P69", r["SchoolQnum"])
                else:
                    set_claim_item_identifier(qnum, "P69", r["SchoolQnum"], "P512", r["DegreeQnum"])
        else:
            if pd.isnull(r["DegreeQnum"]):
                set_claim(qnum, "P69", r["SchoolQnum"])
            else:
                set_claim_item_identifier(qnum, "P69", r["SchoolQnum"], "P512", r["DegreeQnum"])
    elif prop == "P856":
        if not pd.isnull(r["web"]):
            if prop in claims:
                val = 0
                for claim in claims[prop]:
                    target = claim.getTarget()
                    if target == r["web"]:
                        val += 1
                if val == 0:
                    set_claim_url_itentifier(qnum, "P856", r["web"], "P407", "Q1860")
            else:
                set_claim_url_itentifier(qnum, "P856", r["web"], "P407", "Q1860")
    else:
        if prop in claims:
            val = 0
            for claim in claims[prop]:
                target = claim.getTarget()
                objid = target.id
                if objid == obj:
                    val += 1
            if val == 0:
                set_claim(qnum, prop, obj)
        else:
            set_claim(qnum, prop, obj)
    return


def read_csv_tenure(filename, output):
    df = pd.read_csv(filename)
    df1 = df.copy()

    for i, r in df.iterrows():
        if pd.isnull(r["FQnum"]):
            label_dict = {"en": r["FacultyNameForWiki"]}
            des_dict = {"en": "academic"}
            qnum = create_item(site, label_dict, des_dict)
            df1.at[i, "FQnum"] = qnum
            # the first line is subjected to change
            set_claim(qnum, "P101", r["FieldQnum"])
            ###
            set_claim(qnum, "P31", "Q5")
            set_claim(qnum, "P1416", r["Qcol"])
            set_claim(qnum, "P1416", r["Qdept"])
            set_claim(qnum, "P106", "Q1622272")
            set_claim(qnum, "P106", "Q1650915")
            set_claim(qnum, "P108", "Q913861")
            if not pd.isnull(r["SchoolQnum"]):
                if pd.isnull(r["DegreeQnum"]):
                    set_claim(qnum, "P69", r["SchoolQnum"])
                else:
                    set_claim_item_identifier(qnum, "P69", r["SchoolQnum"], "P512", r["DegreeQnum"])
            if not pd.isnull(r["web"]):
                set_claim_url_itentifier(qnum, "P856", r["web"], "P407", "Q1860")
            if not pd.isnull(r["LCnum"]):
                set_claim_external_id(qnum, "P244", r["LCnum"])
        else:
            qnum = r["FQnum"]
            item = pywikibot.ItemPage(repo, qnum)
            claims = item.get()["claims"]
            check_pro_in_sub(qnum, 'P101', r, r["FieldQnum"])
            check_pro_in_sub(qnum, 'P31', r, 'Q5')
            check_pro_in_sub(qnum, 'P1416', r, r["Qcol"])
            check_pro_in_sub(qnum, 'P1416', r, r["Qdept"])
            check_pro_in_sub(qnum, "P106", r, "Q1622272")
            check_pro_in_sub(qnum, "P106", r, "Q1650915")
            if not pd.isnull(r["LCnum"]):
                check_pro_in_sub(qnum, "P244", r, r["LCnum"])
            if not pd.isnull(r["web"]):
                check_pro_in_sub(qnum, "P856", r, r["web"])
            if not pd.isnull(r["SchoolQnum"]):
                check_pro_in_sub(qnum, "P69", r, r["SchoolQnum"])
    df1.to_csv(output)
    return df1


def read_csv_emeritus(filename, output):
    df = pd.read_csv(filename)
    df1 = df.copy()
    for i, r in df.iterrows():
        if pd.isnull(r["FQnum"]):
            label_dict = {"en": r["FacultyNameForWiki"]}
            des_dict = {"en": "academic"}
            qnum = create_item(site, label_dict, des_dict)
            df1.at[i, "FQnum"] = qnum
            # the first line is subjected to change
            set_claim(qnum, "P101", r["FieldQnum"])
            ###
            set_claim(qnum, "P31", "Q5")
            set_claim(qnum, "P106", "Q1622272")
            set_claim(qnum, "P106", "Q1650915")
            set_claim_item_identifier(qnum, "P106", 'Q1240569', "P1027", 'Q913861')
            set_claim(qnum, "P108", "Q913861")
            if not pd.isnull(r["SchoolQnum"]):
                if pd.isnull(r["DegreeQnum"]):
                    set_claim(qnum, "P69", r["SchoolQnum"])
                else:
                    set_claim_item_identifier(qnum, "P69", r["SchoolQnum"], "P512", r["DegreeQnum"])
            if not pd.isnull(r["web"]):
                set_claim_url_itentifier(qnum, "P856", r["web"], "P407", "Q1860")
            if not pd.isnull(r["LCnum"]):
                set_claim_external_id(qnum, "P244", r["LCnum"])
        else:
            qnum = r["FQnum"]
            item = pywikibot.ItemPage(repo, qnum)
            claims = item.get()["claims"]
            check_pro_in_sub(qnum, 'P101', r, r["FieldQnum"])
            check_pro_in_sub(qnum, 'P31', r, 'Q5')
            check_pro_in_sub(qnum, "P106", r, 'Q1240569')
            check_pro_in_sub(qnum, "P106", r, "Q1622272")
            check_pro_in_sub(qnum, "P106", r, "Q1650915")
            if not pd.isnull(r["LCnum"]):
                check_pro_in_sub(qnum, "P244", r, r["LCnum"])
            if not pd.isnull(r["web"]):
                check_pro_in_sub(qnum, "P856", r, r["web"])
            if not pd.isnull(r["SchoolQnum"]):
                check_pro_in_sub(qnum, "P69", r, r["SchoolQnum"])
    df1.to_csv(output)
    return df1


def createWikidataItems(typeFaculty, sourceFilePath, fileName, destination):
    typeOfFaculty = typeFaculty

    source = sourceFilePath+fileName

    newFileName = fileName[:len(fileName) - 4]
    destination = destination+newFileName+'_final.csv'

    if typeOfFaculty == 't':
        read_csv_tenure(source, destination)
    elif typeOfFaculty == 'e':
        read_csv_emeritus(source, destination)
    else:
        return "FAIL: Please enter proper code for type of faculty."

    return "SUCCESS!!!"

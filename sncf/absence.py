# -*- coding: utf-8 -*-
import requests


def getData(url):
    r = requests.get(url, verify=False)
    return r.json()

def main():
    nbAgents = [i['fields'] for i in getData("https://ressources.data.sncf.com/explore/dataset/nombre-total-agents-effectifs/download?format=json")]
    agentsByDate = dict()
    absByDate = dict()
    for i in getData("https://ressources.data.sncf.com/explore/dataset/nombre-total-agents-effectifs/download?format=json"):
        year = i['fields']['date']
        college = i['fields']['college'].encode("utf-8")
        effectif = i['fields']['effectif']
        if year not in agentsByDate:
            agentsByDate[year] = dict()
        if college not in agentsByDate[year]:
            agentsByDate[year][college] = 0
        agentsByDate[year][college] += effectif

    for i in getData("http://ressources.data.sncf.com/explore/dataset/journees-absence-agents/download?format=json"):
        year = i['fields']['date']
        college = i['fields']['college'].encode("utf-8")
        if year not in absByDate:
            absByDate[year] = dict()
        if college not in absByDate[year]:
            if college == "Cadre et cadre supérieur":
                effectif = agentsByDate[year]['Cadres'] + agentsByDate[year]['Cadres supérieurs']
            else:
                effectif = agentsByDate[year][college]
            try:
                absByDate[year][college] = {"total_absence": 0,
                                            "motifs": [],
                                            "effectif": effectif}
            except BaseException, e:
                print "ERROR: %s" % str(e)
                continue
        absByDate[year][college]["total_absence"] += i['fields']['nombre_journees_absence']
        absByDate[year][college]["motifs"].append({"nombre_journees_absence": i['fields']['nombre_journees_absence'],
                                                   "motif": i['fields']['motif']})

    for year in sorted(absByDate.keys()):
        print "Year: %s (nb de jour d'absence moyen)" % year
        for college, i in absByDate[year].iteritems():
            print "\t%s => %.2f" % (college, float(i['total_absence']) / i['effectif'])

if __name__ == "__main__":
    main()



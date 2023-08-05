##------------------------Function Declaration--------------------------------
##Populates the created proxy with manifest flows
def populateFlows(flowNumber, flowList, defaultFlows, manifestFlows):
    for x in range (0, flowNumber):
        for flow in manifestFlows.findall('Flow'):
            if (flow.attrib['name'] == flowList[x]):
                request = flow.find('Request')
                response = flow.find('Response')
                if(request is not None):
                    for child in defaultFlows:
                        if(child.attrib['name'] == flow.attrib['name']):
                            child.append(request)
                if(response is not None):
                    for child in defaultFlows:
                        if(child.attrib['name'] == flow.attrib['name']):
                            child.append(response)
    return defaultFlows


##Makes a list of the flow names in the created proxy

def makeFlowList(flowBulk):
    flowNames = []
    for flow in flowBulk.findall('Flow'):
        flowNames.append(flow.attrib['name'])
    return flowNames

##Cleans the flows in the created proxy
def cleanFlows(flowNumber, flowList, flows):
    for x in range (0, flowNumber):
        for flow in flows.findall('Flow'):
            if (flow.attrib['name'] == flowList[x]):
                for child in flow:
                    tag = str(child.tag)
                    if(tag == 'Request'):
                        flow.remove(child)
                for child in flow:
                    tag = str(child.tag)
                    if(tag == 'Response'):
                        flow.remove(child)    
    return flows
##Preflow and Postflow Cleaner
def cleaner(flow):
    for child in flow:
        tag = str(child.tag)
        if(tag == 'Step'):
            flow.remove(child)
    return flow

## Preflow/Postflow Populate
def populater(manifestFlow, defaultFlow):
    if(manifestFlow is not None):
        for child in manifestFlow:
            defaultFlow.append(child)
    return defaultFlow



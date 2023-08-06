
from matplotlib import pyplot as plt
from alloyml.atomic import prop_value, elements_in


def property_hist(prop, *alloys):
    fig, axs = plt.subplots()
    axs.set_xlabel(prop)
    plt.hist([[prop_value(e, prop) for e in elements_in(a)] for a in alloys],
             weights=[[a[e] for e in elements_in(a)] for a in alloys],
             label=[a.name for a in alloys])
    axs.legend(prop={'size': 10})
    return axs

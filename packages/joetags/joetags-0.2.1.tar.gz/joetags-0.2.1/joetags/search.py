from joetags.core.build import build_tagmap
from joetags.helper.colorprint import wrap_color


def search_interface(args):

    if args.filter == None:
        tagfilter = input("Enter Filter:")
    else:
        tagfilter = args.filter

    search(tagfilter)

    
def search(tagfilter):
    tagmap = build_tagmap()
    results = tagmap.search(tagfilter)
    if len(results) > 0 : 
        print(wrap_color("Results", "green"))
        for result in results:
            print(wrap_color("   " + result, "green"))

    else : print("no results found")
    
    print(wrap_color(tagmap.warning(), "red"))


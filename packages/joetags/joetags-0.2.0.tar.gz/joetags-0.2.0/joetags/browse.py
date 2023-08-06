from joetags.core.build import build_tagmap


def browse(args):

    if args.use_groupname:
        if args.browse_selection != None:
            group = args.browse_selection
            tagmap = build_tagmap()
            tags = tagmap.group_tags(group)
            tagnames = list(map(lambda x: x.name, tags))
            # removes duplicates
            tagnames = list(set(tagnames))

            for tagname in tagnames:
                print(tagname)
        else:
            print("You have to specify a Group Name")
        exit()

    else:
        tagmap = build_tagmap()
        results = []
        if not args.groups and not args.tags:
            # when no group and not tag flag return both
            args.groups = True
            args.tags = True

        if args.groups == True:
            results.extend(tagmap.groups(args.browse_selection))
        if args.tags == True:
            results.extend(tagmap.tags(args.browse_selection))

        # removes all duplicates
        results = list(set(results))

        for result in results:
            print(result)

        exit()



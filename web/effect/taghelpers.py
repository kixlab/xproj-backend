from effect.models import Effect
from taggit.models import Tag
from json import JSONEncoder

class TagTreeEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, TagNode):
            return o.__dict__
        elif isinstance(o, TagTree):
            return self.default(TagTree.root)
        elif isinstance(o, list):
            return JSONEncoder.default(self, [self.default(p) for p in o])
        else:
            return JSONEncoder.default(self, o)

class TagNode:
    tag = ''
    pos_count = 0
    neg_count = 0
    total_count = 0
    children = []
    def __repr__(self):
        return self.tag

    def __init__(self, tag, pos_count = 0, neg_count = 0):
        self.tag = tag
        self.pos_count = pos_count
        self.neg_count = neg_count
        self.total_count = pos_count + neg_count
        self.children = []
        self.pc = 0

    def add_child(self, node):
        if node.tag not in [t.tag for t in self.children]:
            self.children.append(node)

    def add_child_name(self, name, pos_count, neg_count):
        if name not in [t.tag for t in self.children]:
            self.children.append(TagNode(name, pos_count, neg_count))


    def remove_child(self, tag):
        targetIdx = None
        for idx, node in enumerate(self.children):
            if node.tag == tag:
                targetIdx = idx
                break
        if targetIdx is not None:
            self.children.pop(targetIdx)
        
class TagTree:
    root = None
    included_tags = []

    def __init__(self):
        self.root = TagNode('root')
        self.included_tags = []

    def isEmpty(self):
        return len(self.included_tags) <= 0

    def construct_tag_tree(self, tag_list):
        sorted_tags = sorted(tag_list, key = lambda x: x[1], reverse = True)

        while len(sorted_tags) > 0:
            tags_list = [x[0] for x in sorted_tags]
            ele = sorted_tags.pop(0) # pick the most referenced one
            queryset_level1 = Effect.objects.filter(tags__name__in=[ele[0]]).filter(is_guess = False)
            level1_node = TagNode(ele[0], ele[2], ele[3])
            self.included_tags.append(ele[0])
            # self.root.add_child(level1_node)

            # possible_children = list(queryset_level1.values('tags__name')) # extract possible childs
            # possible_children_text = list(set([tag for tag in possible_children['tags__name']]))
            # level1_node.pc = possible_children
            for t in tags_list:
                if t in self.included_tags:
                    continue
                
                t12 = queryset_level1.filter(tags__name__in=[t])
                # t12_count = t12.count()
                t12_pos_count = t12.filter(is_benefit = True).count()
                t12_neg_count = t12.filter(is_benefit = False).count()

                if (t12_neg_count + t12_pos_count) > 0:
                    level1_node.add_child_name(t[0], t12_pos_count, t12_neg_count)
            #    t2 = None
            #    t2idx = None
            #    for idx, tag in enumerate(sorted_tags):
            #        if tag[0] == t:
            #            t2idx = idx
            #            t2 = tag 
            #    if t2 is None:
            #        continue

            #    t2_count = t2[1]
            #    if t12_count >= 0.85 * t2_count:
            #        level1_node.add_child_name(t2[0], t2[2], t2[3])
            #        sorted_tags.pop(t2idx)

            self.root.add_child(level1_node)

def decide_inclusion(tag1, tag2):
    queryset = Effect.objects.all()
    tag1_count = queryset.filter(tags__name__in=[tag1]).count()
    tag2_count = queryset.filter(tags__name__in=[tag2]).count()
    tag12_count = queryset.filter(tags__name__in=[tag1, tag2]).count()

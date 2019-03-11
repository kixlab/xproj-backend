from effect.models import Effect
from taggit.models import Tag
from json import JSONEncoder

class TagTreeEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, TagNode):
            return o.__dict__
        elif isinstance(o, TagTree):
            return self.default(TagTree.root)
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
    
    def add_child(self, node):
        if node not in self.children:
            self.children.append(node)

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

    def construct_tag_tree(self, tag_list):
        sorted_tags = sorted(tag_list, key = lambda x: x[1], reverse = True)
        queryset = Effect.objects.all()

        while len(sorted_tags) > 0:
            ele = sorted_tags.pop(0) # pick the most referenced one

            level1_node = TagNode(ele[0], ele[2], ele[3])
            self.root.add_child(level1_node)

            possible_children = list(queryset.filter(tags__name__in=[ele[0]]).values_list('tags', flat=True)) # extract possible childs
            possible_children_text = list(set([tag for tag in possible_children]))
            queryset_level1 = queryset.filter(tags__name__in=[ele[0]])
            for t in possible_children_text:
                if t in self.included_tags:
                    continue
                t12_count = queryset_level1.filter(tags__name__in=[t])
                t2 = [elem for elem in sorted_tags if elem[0] == t]
                if len(t2) <= 0:
                    continue
                t2_count = t2[0][1]
                if t12_count >= t2_count * 0.9:
                    level1_node.add_child(TagNode(t2[0][0], t2[0][2], t2[0][3]))
                    sorted_tags.remove(t2)


def decide_inclusion(tag1, tag2):
    queryset = Effect.objects.all()
    tag1_count = queryset.filter(tags__name__in=[tag1]).count()
    tag2_count = queryset.filter(tags__name__in=[tag2]).count()
    tag12_count = queryset.filter(tags__name__in=[tag1, tag2]).count()

from Cheetah.Template import Template

def nsTxt(ns, template):
    return str(Template(template, ns))

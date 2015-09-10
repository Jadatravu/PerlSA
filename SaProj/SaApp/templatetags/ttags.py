from django import template

register = template.Library()

@register.simple_tag(takes_context = True)
def change_file_path (context,path_str):
    res_str=str(path_str).replace('^','/')
    return res_str

@register.simple_tag(takes_context = True)
def add_builds_table(context,dic):
    res_str=str('')
    build_dic_list = dic
    build_id_list = [] 
    for key,value in build_dic_list.items():
        build_id_list.append(key)
    build_id_list.sort()
    earlier_build_name=str('')
    for id in build_id_list: 
       for key,value in build_dic_list.items():
           if key == id:
              if earlier_build_name == '':
                  build_issue_link = str("<a>None</a>")
              else:
                  build_issue_link = str("<a href=/issue_bet_builds/?build1=")+str(earlier_build_name) + str("&build2=") + str(value["name"]) + str("> issues link</a>")
              res_str += str("<tr><td></td><td>") + value["name"] + str("</td><td>")+str(value['revision']) +str("</td><td>") + str(value["issues"]) + str("</td><td>") + str(build_issue_link)+str("</td></tr>")
              earlier_build_name = value["name"]
    return res_str

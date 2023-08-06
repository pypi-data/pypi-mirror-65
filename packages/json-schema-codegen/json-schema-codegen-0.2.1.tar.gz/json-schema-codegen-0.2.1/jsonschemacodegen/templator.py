import os
import jinja2
import stringcase
import re

PLANTUML_REPLACE = re.compile(r"```plantuml\n(.*)```", re.DOTALL|re.MULTILINE)

class Generator(object):

    def __init__(self, templatePkg, outputDir):
        self.templatePkg = templatePkg
        self.outputDir = outputDir
        self.generatedFiles = []
        self.jinjaEnvironment = None

    def GetJinjaEnvironment(self):
        def IsOfType(obj, theType):
            return theType in str(type(obj))

        def AddLeadingUnderscore(s: str):
            return "_%s" % (s)

        def Privatize(s: str):
            return AddLeadingUnderscore(stringcase.camelcase(s))

        def QuoteIfString(s: str, condition):
            if condition == 'string' or isinstance(condition, str):
                return '"%s"' % (s)
            return s

        def Enumify(s: str):
            if s[0].isnumeric():
                return "_"+stringcase.constcase(s)
            return stringcase.constcase(s)

        def UpperCamelCase(s: str):
            return stringcase.pascalcase(stringcase.snakecase(s)).replace('_', '')

        def MdIndent(s: str, width: int):
            indention = " " * width
            newline = "\n"

            s += newline  # this quirk is necessary for splitlines method

            lines = s.splitlines()
            rv = lines.pop(0)

            if lines:
                rv += newline + newline.join(
                    indention + line if (line and not line.strip().startswith('<')) else line for line in lines
                )

            return rv

        def Italics(s: str):
            if s and s is not None and s != 'None' and len(s) > 0:
                return "_%s_" % (s)
            else:
                return ''

        def Doxygenify(s: str):
            if "```plantuml" in s:
                return PLANTUML_REPLACE.sub(r"\\startuml\n\1\\enduml", s)
            return s

        if self.jinjaEnvironment is None:
            env = jinja2.Environment(loader=jinja2.PackageLoader(self.templatePkg, ''),
                                     extensions=['jinja2.ext.do'])
            env.filters['UpperCamelCase'] = UpperCamelCase
            env.filters['PascalCase'] = lambda s: stringcase.pascalcase(stringcase.snakecase(s))
            env.filters['CONST_CASE'] = lambda s : stringcase.constcase(str(s))
            env.filters['snake_case'] = stringcase.snakecase
            env.filters['camelCase'] = stringcase.camelcase
            env.filters['mdindent'] = MdIndent
            env.filters['type'] = type # For debugging
            env.filters['doxygen'] = Doxygenify
            env.filters['italics'] = Italics
            env.filters['quotestring'] = QuoteIfString
            env.filters['dir'] = dir # For debug
            env.filters['privatize'] = Privatize
            env.filters['enumify'] = Enumify
            env.tests['oftype'] = IsOfType
            self.jinjaEnvironment = env
        return self.jinjaEnvironment

    def GetRenderedTemplate(self, template_name, **kwargs):
        template = self.GetJinjaEnvironment().get_template(template_name)
        rendered = template.render(kwargs)
        return rendered

    def RenderTemplate(self, template_name, output_name = None, **kwargs):
        output_filename = output_name or ".".join(template_name.split(".")[:-1])
        output_file = os.path.join(self.outputDir, output_filename)
        rendered = self.GetRenderedTemplate(template_name, **kwargs)
        with open(output_file, "w") as fp:
            fp.write(rendered)
        self.generatedFiles.append(output_filename)

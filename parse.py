#!/usr/bin/env python
#coding: utf8

from __future__ import division
import pytoml
import datetime
import textwrap


# Map month names to numbers
MONTHS = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12
}

# Map computer skill numbers to words
SKILL_LEVEL = {
    1 : "basics",
    2 : "good",
    3 : "excellent"
}

# Map language skill numbers to words
LANGUAGE_SKILL = {
    1 : "basic",
    2 : "good",
    3 : "fluent",
    4 : "native"
}

# Make a data structure for a job, this is just so that sorting
# a list of jobs in time order becomes easier.
class Job:
    def __init__(self, job_dict):
        self.title = job_dict["title"]
        self.employer = job_dict["where"]
        start = job_dict["start"]
        end = job_dict["end"]
        if "preposition" in  job_dict.keys():
            self.preposition = job_dict["preposition"]
        else:
            self.preposition = "at"
        if type(start) is datetime.datetime:
            self.start = start
            self.str_start = start.strftime("%B %Y")
        elif type(start) is str:
            self.start = datetime_from_string(start)
            self.str_start = start
        if type(end) is datetime.datetime:
            self.end = end
            self.str_end = end.strftime("%B %Y")
        elif type(end) is str:
            self.end = datetime_from_string(end)
            self.str_end = end
        if "description" in job_dict.keys():
            self.description = "\n" + textwrap.fill(job_dict["description"], 70) + "\n"
        else:
            self.description = ""
    def __cmp__(self, other):
        """Compare two jobs by their starting date."""
        if self.start > other.start:
            return 1
        elif self.start == other.start:
            return 0
        elif self.start < other.start:
            return -1
        else:
            raise ValueError("Failed to compare job starting dates.")
    def to_markdown(self):
        return "### %s %s %s\n\n%s to %s.\n%s" % (self.title, self.preposition, self.employer, self.str_start, self.str_end, self.description)



def datetime_from_string(date):
    if date.strip().lower() == "present":
        return datetime.datetime.now()
    sdate = date.split()
    if len(sdate) == 2:
        month, year = [s.lower() for s in sdate]
        Y = int(year)
        M = MONTHS[month]
    elif len(sdate) == 1:
        Y = int(date)
        M = 1
    return datetime.datetime(Y, M, 1)
    
    

def date_to_string(date):
    if type(date) is datetime.datetime:
        return date.strftime("%d.%m.%Y")
    elif type(date) is str:
        return date
    else:
        raise ValueError("Unknown date format.")

    
    

def resume_to_Markdown(contents, only_tags=None):
    """Parse a resume from TOML and output MarkDown to standard output."""
    sections = contents.keys()
    personal = contents["personal"]
    if "title" in contents.keys():
        print "# %s for %s\n" % (contents["title"], personal["name"])
    else:
        print "# %s\n" % (personal["name"])

    ## PERSONAL BLOCK
    # Handle birthday
    if "birthday" in personal.keys():
        date = personal["birthday"]
        date_txt = date_to_string(date)
        print "DATE OF BIRTH: %s" % date_txt
        print
    
    # Handle address, possibly multiline
    if "address" in personal.keys():
        address = personal["address"]
        print "ADDRESS:"
        if type(address) is list:
            for line in address:
                print "    %s" % (line)
        elif type(address) is str:
            print "    %s" % (address)
        print
    
    # Handle phone number
    if "phone" in personal.keys():
        print "PHONE: %s" % personal["phone"]
        print

    # Handle email address
    if "email" in personal.keys():
        print "EMAIL: <%s>" % personal["email"]
        print
            

    ## EDUCATION BLOCK
    if "education" in sections:
        education = contents["education"]
        print "\n## Education"
        print
        for key in education.keys():
            degree = education[key]
            # Print title
            if "field" in degree.keys():
                line = "### %s in %s" % (degree["title"], degree["field"])
            else:
                line = "### %s" % (degree["title"])
            print line
            print
    
            # Handle institution
            if "where" in degree.keys():
                print "From %s." % degree["where"]
    
            # Handle start and end dates
            has_start = False
            has_end = False
            if "start" in degree.keys():
                has_start = True
                start = date_to_string(degree["start"])
            if "end" in degree.keys():
                has_end = True
                end = date_to_string(degree["end"])
            if has_start and has_end:
                print "Started: %s" % (start)
            elif has_end:
                print "Completed: %s" % (end)
            print 
            if "description" in degree.keys():
                print textwrap.fill(degree["description"], 70)
                print
    
    ## WORK BLOCK
    if "work" in sections:
        work = contents["work"]
        print "\n## Work experience"
        print
        jobs = [Job(x) for x in work.values()]
        for job in sorted(jobs):
            if only_tags:
                for tag in only_tags:
                    if tag in job.tags:
                        print job.to_markdown()
            else:
                print job.to_markdown()

    ## SKILLS BLOCK
    if "skills" in sections:
        skills = contents["skills"]
        print "\n## Skills"
        if "computer" in skills.keys():
            print "\n### Computer skills\n"
            computer_skills = skills["computer"]
            # Sort computer skills by skill level
            c_list = []
            for skill, value in computer_skills.iteritems():
                c_list.append((value, skill.replace("_", " ")))
            c_list.sort()
            c_list.reverse()
            for skill in c_list:
                print "- %s (%s)" % (skill[1], SKILL_LEVEL[skill[0]])
        if "language" in skills.keys():
            print "\n### Languages\n"
            languages = skills["language"]
            # Sort languages by the mean of written and oral skill
            c_list = []
            for language in languages.keys():
                written = languages[language]["written"]
                oral = languages[language]["oral"]
                avg = (written+oral) / 2
                c_list.append((avg, language, written, oral))
            c_list.sort()
            c_list.reverse()
            for avg, language, written, oral in c_list:
                if written == oral:
                    print "- %s: written and oral: %s" % (language, LANGUAGE_SKILL[written])
                else:
                    print "- %s: written %s, oral %s" % (language, LANGUAGE_SKILL[written], LANGUAGE_SKILL[oral])
        if "other" in skills.keys():
            print "\n### Other skills\n"
            other = skills["other"]
            for skill in other:
                print "- %s" % (skill)
        print

    ## EXTRACURRICULAR ACTIVITIES BLOCK
    # These are treated just like jobs.
    if "extra" in sections:
        extra = contents["extra"]
        print "\n## Extracurricular activities"
        print
        jobs = [Job(x) for x in extra.values()]
        for job in sorted(jobs):
            if only_tags:
                for tag in only_tags:
                    if tag in job.tags:
                        print job.to_markdown()
            else:
                print job.to_markdown()


if __name__ == "__main__":
    from sys import argv, exit
    
    if len(argv) > 1:
        parser = pytoml.Parser()
        parser.read(argv[1])
        resume_to_Markdown(parser.content)
        exit(0)
    else:
        exit(1)
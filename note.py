from collections import UserDict
from datetime import datetime
from csv import DictReader, DictWriter
import re


class Field:
    def __init__(self, text):
        self.text = text

    def __str__(self) -> str:
        return str(self.text)


class Title(Field):
    def __init__(self, title):
        self.text = title


class Tag(Field):
    def __init__(self, tag) -> None:
        self.text = tag


class Notation(Field):
    def __init__(self, title) -> None:
        self.text = title


class Record:
    def __init__(self):
        self.title = None
        self.tag = []
        self.note = None
        self.date = datetime.now().strftime("%d.%m.%Y %H:%M")

    def add_title(self, title):
        self.title = Title(title)

    def add_tag(self, tags):
        if isinstance(tags, list):
            for t in tags:
                self.tag.append(Tag(t))
        elif isinstance(tags, str) and len(tags.split(",")) > 1:
            for t in tags.split(","):
                self.tag.append(Tag(t))
        else:
            self.tag.append(Tag(tags))

    def add_note(self, note):
        if len(note) <= 256:
            self.note = Notation(note)
        else:
            raise ValueError("Too mach symbols. 256 symbols are allowed")

    def edit_note(self, new_note):
        self.add_note(new_note)

    def create_record(self, text):
        self.add_title(self.find_title_in_text(text))
        self.add_tag(self.find_tags_in_text(text))
        self.add_note(self.find_note_in_text(text))

    def find_title_in_text(self, text):
        try:
            title = re.findall(r"(?<!#)\b[A-Z]+\b", text)
            return " ".join(title)
        except ValueError:
            print("No title found")
            return []

    def find_tags_in_text(self, text):
        try:
            tags = re.findall(r"#\w+", text)
            return tags
        except ValueError:
            print("No tags found")
            return []

    def find_note_in_text(self, text):
        try:
            pattern = re.compile(r"(?<!#)\b[A-Z]+\b")
            text = pattern.sub("", text)
            pattern = re.compile(r"#\w+")
            text = pattern.sub("", text)
            note = re.findall(r"\b\S.[^ ]*\b", text)
            return " ".join(note)
        except ValueError:
            print("No note found")
            return []

    def __str__(self) -> str:
        message = ("-" * 148) + "\n"
        if self.title:
            message += "|{:<15}|{:<130}|\n".format("Title", (self.title.text))
            message += ("-" * 148) + "\n"
        if self.note:
            message += "|{:<15}|{:<130}|\n".format("Notice", (self.note.text))
            message += ("-" * 148) + "\n"
        if self.tag:
            message += "|{:<15}|{:<130}|\n".format(
                "Tags", (" ".join(t.text for t in self.tag))
            )
        message += ("-" * 148) + "\n"
        message += "|{:<15}|{:<130}|\n".format("Date", (self.date))
        message += ("-" * 148) + "\n"
        return message


class NoteData(UserDict):
    def add_record(self, note):
        self.data[note.title.text] = note

    def delete(self, note_name):
        if note_name in self.data:
            del self.data[note_name]

    def find_note(self, word):
        if len(word) >= 3:
            pattern = re.compile(word.lower())
            result = []
            if re.match(r"\d{2}.\d{2}.\d{4}", word):
                for note in self.data:
                    if word == self.data[note].date.split(" ")[0]:
                        result.append(self.data[note])
                return result
            else:
                for note in self.data:
                    note_find = re.findall(pattern, self.data[note].note.text.lower())
                    title_find = re.findall(pattern, self.data[note].title.text.lower())
                    tag_find = re.findall(
                        pattern,
                        "".join(p.text.lower() for p in self.data[note].tag),
                    )
                    date_find = re.findall(pattern, self.data[note].date)
                    if (
                        len(note_find) > 0
                        or len(title_find) > 0
                        or len(tag_find) > 0
                        or len(date_find) > 0
                    ):
                        result.append(self.data[note])
                    else:
                        continue
                return result
        else:
            raise ValueError("Search word schud have at least 3 characters")

    def to_dict(self, obj=None):
        note_list = []
        if obj is None:
            for rec in self.data:
                note_dict = {
                    "title": self.data[rec].title.text,
                    "tag": ", ".join(p.text for p in self.data[rec].tag),
                    "note": self.data[rec].note.text,
                    "date": self.data[rec].date,
                }
                note_list.append(note_dict)
        else:
            for rec in obj:
                note_dict = {
                    "title": rec.title.text,
                    "tag": ", ".join(p.text for p in rec.tag),
                    "note": rec.note.text,
                    "date": rec.date,
                }
                note_list.append(note_dict)
        return note_list

    def red_csv_file(self, file):
        with open(file, "r") as f:
            dict_reader = DictReader(f, delimiter=";")
            note_data = list(dict_reader)

        for note in note_data:
            for key, value in note.items():
                if key == "title":
                    record = Record()
                    record.add_title(value)
                elif key == "tag":
                    if len(value.split(",")) > 1:
                        for v in value.split(","):
                            record.add_tag(v.strip())
                    else:
                        record.add_tag(value)
                elif key == "note":
                    if note[key]:
                        record.add_note(value)
                    else:
                        continue
                elif key == "date":
                    if note[key]:
                        record.date = value
                    else:
                        continue
                else:
                    continue
                self.add_record(record)

    def write_csv_file(self, file):
        field_names = ["title", "note", "tag", "date"]
        users_list = self.to_dict()
        with open(file, "w") as csvfile:
            writer = DictWriter(csvfile, fieldnames=field_names, delimiter=";")
            writer.writeheader()
            writer.writerows(users_list)


if __name__ == "__main__":
    notebook = NoteData()
    notebook.red_csv_file("fake_note.csv")
    first_notation = Record()
    first_notation.add_title("ЗДАЧА ПРОЕКТУ ПО ГІДРОДИНАМІЦІ")
    first_notation.add_note(
        "Треба виконати проект по темі “……..“ Попередній захист в 4 корпусі 201 кабінет……"
    )
    first_notation.add_tag("#ЛАБА, #20БАЛІВ")
    first_notation.add_tag("#ПАХТ")
    print(first_notation.date)

    first_notation = Record()
    first_notation.create_record(
        """
                                 PROJECT SUBMISSION FOR HYDRODYNAMICS #PAKHT, #LABA, #20POINTS 
                                 It is necessary to complete a project on the topic "......" 
                                 Preliminary defense in the 4th building, room 201..."""
    )
    notebook.add_record(first_notation)

    #    print(first_notation)

    second_notation = Record()
    second_notation.create_record(
        """LIST TO DO #koliu, #goit not so important 5463899"""
    )
    notebook.add_record(second_notation)

    #    print(notebook.to_dict())
    first_find = notebook.find_note("31.10.2023")
    #    print(notebook.to_dict(first_find))

    second_find = notebook.find_note("200")

    dict_result = notebook.to_dict(second_find)

    for r in second_find:
        print(str(r))

    first_notation.edit_note(
        "It is necessary to complete"
    )
    print(first_notation)

    notebook.add_record(first_notation)
    print(notebook.to_dict(first_find))

    print(notebook.find_note("Almost election."))
    notebook.delete("Almost election.")
    print(notebook.find_note("Almost election."))

    print("Hier ist the full list: \n")
    for name, record in notebook.data.items():
        print(str(record) + "\n")

    notebook.write_csv_file("fake_note.csv")

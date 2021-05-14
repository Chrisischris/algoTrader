from auth.const import OUTPUT_PATH
import os


class CSVBuilder:
    def __init__(self, fields: list, filename: str):
        self.field = fields
        self.outputFilePath = os.path.join(OUTPUT_PATH, filename + ".csv")
        self.f = open(self.outputFilePath, "w")
        for f in fields:
            self.f.write(f + ", ")
        self.f.write("\n")
        self.f.close()

    def write(self, fieldValues: list):
        self.f = open(self.outputFilePath, "a")
        for f in fieldValues:
            self.f.write(str(f) + ", ")
        self.f.write("\n")
        self.f.close()

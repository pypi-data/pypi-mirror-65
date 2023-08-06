import json
import abc


class Format:
    @abc.abstractclassmethod
    def load_from_stream(cls, stream):
        pass

    @abc.abstractclassmethod
    def save_to_stream(cls, dct, stream):
        pass

    @classmethod
    def load(cls, f_name):
        with open(f_name) as stream:
            return cls.load_from_stream(stream)

    @classmethod
    def save(cls, dct, f_name):
        with open(f_name, "w") as stream:
            cls.save_to_stream(dct, stream)


class JSON(Format):
    class Encoder(json.JSONEncoder):
        def default(self, o):  # pylint: disable=method-hidden
            return str(o)

    @classmethod
    def load_from_stream(cls, stream):
        return json.load(stream)

    @classmethod
    def save_to_stream(cls, dct, stream):
        json.dump(dct, stream, indent=4, sort_keys=True, cls=cls.Encoder)

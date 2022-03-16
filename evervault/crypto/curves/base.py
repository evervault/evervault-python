from pyasn1.type import univ
from pyasn1.type.namedtype import NamedTypes, NamedType, OptionalNamedType

PUBLIC_KEY_TYPE = (1, 2, 840, 10045, 2, 1)
PRIME_FIELD = (1, 2, 840, 10045, 1, 1)


class Curve(univ.Sequence):
    componentType = NamedTypes(
        NamedType("a", univ.OctetString()),
        NamedType("b", univ.OctetString()),
        OptionalNamedType("seed", univ.BitString()),
    )


class FieldID(univ.Sequence):
    componentType = NamedTypes(
        NamedType("fieldType", univ.ObjectIdentifier()),
        NamedType("parameters", univ.Integer()),
    )


class ECParameters(univ.Sequence):
    componentType = NamedTypes(
        NamedType("version", univ.Integer(1)),
        NamedType("fieldID", FieldID()),
        NamedType("curve", Curve()),
        NamedType("base", univ.OctetString()),
        NamedType("order", univ.Integer()),
        OptionalNamedType("cofactor", univ.Integer()),
    )


class AlgorithmIdentifier(univ.Sequence):
    componentType = NamedTypes(
        NamedType("algorithm", univ.ObjectIdentifier()),
        NamedType("parameters", ECParameters()),
    )


class SubjectPublicKeyInfo(univ.Sequence):
    componentType = NamedTypes(
        NamedType("algorithm", AlgorithmIdentifier()),
        NamedType("subjectPublicKey", univ.BitString()),
    )


class CurveInfo:
    def __init__(self, p, a, b, seed, generator, n, h):
        self.p = p
        self.a = a
        self.b = b
        self.seed = seed
        self.generator = generator
        self.n = n
        self.h = h


class PublicKey:
    def __init__(self, public_key, curve_info):
        self.public_key = public_key
        self.curve_info = curve_info
        self.spki = self.build_encoder()

    def build_encoder(self):
        curve = Curve()
        curve.setComponentByName(
            "a",
            univ.OctetString(hexValue=self.curve_info.a),
        )
        curve.setComponentByName(
            "b",
            univ.OctetString(hexValue=self.curve_info.b),
        )
        curve.setComponentByName(
            "seed", univ.BitString("'{}'H".format(self.curve_info.seed))
        )

        field_id = FieldID()
        field_id.setComponentByName("fieldType", univ.ObjectIdentifier(PRIME_FIELD))
        field_id.setComponentByName(
            "parameters",
            univ.Integer(int(self.curve_info.p, 16)),
        )

        ec_parameters = ECParameters()
        ec_parameters.setComponentByName("fieldID", field_id)
        ec_parameters.setComponentByName("curve", curve)
        ec_parameters.setComponentByName(
            "base", univ.OctetString(hexValue=self.curve_info.generator)
        )
        ec_parameters.setComponentByName(
            "order", univ.Integer(int(self.curve_info.n, 16))
        )
        ec_parameters.setComponentByName("cofactor", univ.Integer(self.curve_info.h))

        algorithm_identifier = AlgorithmIdentifier()
        algorithm_identifier.setComponentByName(
            "algorithm", univ.ObjectIdentifier(PUBLIC_KEY_TYPE)
        )
        algorithm_identifier.setComponentByName("parameters", ec_parameters)

        subject_public_key_info = SubjectPublicKeyInfo()
        subject_public_key_info.setComponentByName("algorithm", algorithm_identifier)
        subject_public_key_info.setComponentByName(
            "subjectPublicKey", univ.BitString("'{}'H".format(self.public_key))
        )

        return subject_public_key_info

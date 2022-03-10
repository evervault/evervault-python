from pyasn1.type import univ, namedtype
from pyasn1.type.namedtype import NamedTypes, NamedType, OptionalNamedType
from pyasn1.codec.der import encoder
import base64

class Curve(univ.Sequence):
  componentType = NamedTypes(
    NamedType('a', univ.OctetString()),
    NamedType('b', univ.OctetString()),
    OptionalNamedType('seed', univ.BitString())
  )

class FieldID(univ.Sequence):
  componentType = NamedTypes(
    NamedType('fieldType', univ.ObjectIdentifier()),
    NamedType('parameters', univ.Integer())
  )

class ECParameters(univ.Sequence):
  componentType = NamedTypes(
    NamedType('version', univ.Integer(1)),
    NamedType('fieldID', FieldID()),
    NamedType('curve', Curve()),
    NamedType('base', univ.OctetString()),
    NamedType('order', univ.Integer()),
    OptionalNamedType('cofactor', univ.Integer()),
  )

class AlgorithmIdentifier(univ.Sequence):
  componentType = NamedTypes(
    NamedType('algorithm', univ.ObjectIdentifier()),
    NamedType('parameters', ECParameters())
  )

class SubjectPublicKeyInfo(univ.Sequence):
    componentType = NamedTypes(
      NamedType('algorithm', AlgorithmIdentifier()),
      NamedType('subjectPublicKey', univ.BitString())
    )

def encode_p256_public_key(public_key):
  curve = Curve()
  curve.setComponentByName('a',univ.OctetString(
    hexValue='FFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC'
  ))
  curve.setComponentByName('b',univ.OctetString(
    hexValue='5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B'
  ))
  curve.setComponentByName('seed',univ.BitString("'C49D360886E704936A6678E1139D26B7819F7E90'H"))

  field_id = FieldID()
  field_id.setComponentByName('fieldType', univ.ObjectIdentifier((1,2,840,10045,1,1)))
  field_id.setComponentByName('parameters', univ.Integer(
    int('FFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF',16)
  ))

  ec_parameters = ECParameters()
  ec_parameters.setComponentByName('fieldID', field_id)
  ec_parameters.setComponentByName('curve', curve)
  ec_parameters.setComponentByName('base', univ.OctetString(
    hexValue='046B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C2964FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5'
  ))
  ec_parameters.setComponentByName('order', univ.Integer(
    int('FFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551',16)
  ))
  ec_parameters.setComponentByName('cofactor', univ.Integer('01'))

  algorithm_identifier = AlgorithmIdentifier()
  algorithm_identifier.setComponentByName('algorithm', univ.ObjectIdentifier((1,2,840,10045,2,1)))
  algorithm_identifier.setComponentByName('parameters', ec_parameters)

  subject_public_key_info = SubjectPublicKeyInfo()
  subject_public_key_info.setComponentByName('algorithm', algorithm_identifier)
  subject_public_key_info.setComponentByName('subjectPublicKey', univ.BitString("'{}'H".format(public_key)))

  return encoder.encode(subject_public_key_info)

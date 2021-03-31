const crypto = require('crypto');

const datatypes = ['string', 'number', 'bignumber', 'boolean'];

function decrypt(payload="ev:FsZZjYZgG4uvAUBY:AmGiQTj8tOB/pXxHn3J+PLX1HpGaYcgymJkcGCUsNp8U:CrqvlV4gi9ZYfv0liuED1E+X9GtD:$") {
  const sections = payload.split(':');
  const typ = {
    datatype: datatypes.includes(sections[1]) ? sections[1] : 'string',
    keyIv: datatypes.includes(sections[1]) ? sections[2] : sections[1],
    ecdhPublicKey: datatypes.includes(sections[1]) ? sections[3] : sections[2],
    aesEncryptedData: datatypes.includes(sections[1]) ? sections[4] : sections[3],
  }

  const [authTag, trimmedData] = extractAuthTag(typ.aesEncryptedData);
  const ecdh = crypto.createECDH('secp256k1');
  ecdh.setPrivateKey(base64ToBuffer('7yoUeVQ9gKwcJUwwlfUSSvgGq207A8yz8siy0G7tXi8='))
  const derivedSecret = ecdh.computeSecret(Buffer.from(typ.ecdhPublicKey, 'base64'));
  const decipherer = crypto.createDecipheriv(
    'aes-256-gcm',
    derivedSecret,
    Buffer.from(typ.keyIv, 'base64')
  );
  decipherer.setAuthTag(authTag);
  let decryptedData = decipherer.update(
    base64ToBuffer(trimmedData),
    'base64',
    'utf8'
  );
  decryptedData += decipherer.final('utf8');
  console.log("HERE", decryptedData);
}

const base64ToBuffer = (b64String, validateBase64 = false) => {
  if (!validateBase64 || isBase64(b64String)) {
    return Buffer.from(b64String, 'base64');
  }
  throw new Error('Expected string to be base 64 encoded');
};

function extractAuthTag(encryptedData, authTagLength = 128) {
  const dataBuffer = Buffer.from(encryptedData, 'base64');
  console.log("dataBuffer", dataBuffer.length);
  const authTagFirstByte = dataBuffer.byteLength - authTagLength / 8;
  console.log("authTagFByte", authTagFirstByte);
  const authTag = dataBuffer.slice(authTagFirstByte);
  const trimmedData = dataBuffer.slice(0, authTagFirstByte);
  return [authTag, trimmedData];
}

const generateEcdhPair = () => {
  // Using P-256 curve instead of P-384, as keys are
  // 16 bytes shorted with no significant security
  // reduction. Change to Curve25519 once it is supported
  // more broadly in Web Crypto.
  const ecdh = crypto.createECDH('secp256k1');
  ecdh.generateKeys();
  const pk = ecdh.getPublicKey(null, 'compressed').toString('base64');
  console.log(`Server PublicKey: ${pk}`)
  console.log(`Server PrivateKey: ${ ecdh.getPrivateKey(null, 'compressed').toString('base64')}`)
  return ecdh;
};

console.log(decrypt());
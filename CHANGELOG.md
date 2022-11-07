# Changelog

<!--next-version-placeholder-->

## v1.3.2 (2022-11-07)
### Fix
* Replace recursive timer call with RepeatedTimer class ([#78](https://github.com/evervault/evervault-python/issues/78)) ([`cf22d6c`](https://github.com/evervault/evervault-python/commit/cf22d6c0e8c352d6228497efd0f4e8babdff0769))

## v1.3.1 (2022-11-04)
### Fix
* Store thread spawing on each call to init ([#77](https://github.com/evervault/evervault-python/issues/77)) ([`e5ae0e1`](https://github.com/evervault/evervault-python/commit/e5ae0e1ef3fbb750cc8dc7bb396fd022e18c8603))

## v1.3.0 (2022-10-27)
### Feature
* Poll the Evervault API for relay outbound configuration ([#74](https://github.com/evervault/evervault-python/issues/74)) ([`e1cbfb4`](https://github.com/evervault/evervault-python/commit/e1cbfb4694ee37140880cfb3b850c91be8a52f8b))

## v1.2.1 (2022-09-23)
### Fix
* Empty proxies for each request ([`8d9c6a2`](https://github.com/evervault/evervault-python/commit/8d9c6a2d536d98dacb295b4c4595a79f384ac499))

## v1.2.0 (2022-09-05)
### Feature
* **create_run_token:** Adding create_run_token ([`177236a`](https://github.com/evervault/evervault-python/commit/177236a944de99e9ea5278123a3e96e9a7b82c35))

### Documentation
* **createruntoken:** Describing run tokens ([`e8ee900`](https://github.com/evervault/evervault-python/commit/e8ee900f10d8ac61905fa89735db54b227ae3742))

## v1.1.0 (2022-07-20)
### Feature
* **outbound:** Supports wildcard decryption domains ([`dbdf279`](https://github.com/evervault/evervault-python/commit/dbdf2796a6a9bbef43536186399daa0d1b658777))

### Documentation
* Adds wildcard reference ([`5d7bfc7`](https://github.com/evervault/evervault-python/commit/5d7bfc7e440de2690beca949a2ff177758d704a3))

## v1.0.0 (2022-07-06)
### Feature
* Supports decrypt_domains config option ([`1a69cce`](https://github.com/evervault/evervault-python/commit/1a69cce6254ba09d62510b2ff3adc9b8a2def22b))

### Breaking
* Traffic won't be sent through outbound proxy by default anymore  ([`1a69cce`](https://github.com/evervault/evervault-python/commit/1a69cce6254ba09d62510b2ff3adc9b8a2def22b))

## v0.8.4 (2022-06-30)
### Fix
* Merge pull request #67 from evervault/eoinpm/pro-989-end-the-ddos-machine-python-sdk ([`06d0d05`](https://github.com/evervault/evervault-python/commit/06d0d05bca35b9e4f19568e4d9087dff2c296b25))
* Keeps static link to requests.Session.request ([`65a281c`](https://github.com/evervault/evervault-python/commit/65a281c0cab89df19d8f40e22aab9bb519f75eb9))

## v0.8.3 (2022-06-29)
### Fix
* Respect ignore domains list ([`6fd9e49`](https://github.com/evervault/evervault-python/commit/6fd9e49051ba6c0ab016b0b4c38d4d92d86380b2))

## v0.8.2 (2022-05-12)
### Fix
* Format ([`e3010a9`](https://github.com/evervault/evervault-python/commit/e3010a961c26a9d8c0804e1e6a377e1816258ad0))
* Remove metrics ([`ade1ff9`](https://github.com/evervault/evervault-python/commit/ade1ff9ddfad9d231cbd8c4d83d33d609c0ba42a))

## v0.8.1 (2022-05-04)
### Fix
* **crypto client:** Dont add AAD when using K1 curve ([`bcb5548`](https://github.com/evervault/evervault-python/commit/bcb5548a9b1f468f604e353155179a40943f044a))

## v0.8.0 (2022-04-13)
### Feature
* Implement latest crypto scheme support adding KDF to derived secret keys ([`f7c5e49`](https://github.com/evervault/evervault-python/commit/f7c5e496508b0b31f570b14e8bffb4c2fccb2e77))
* Add option for P256 curve in init function while keeping old curve as default ([`98b709c`](https://github.com/evervault/evervault-python/commit/98b709ca39f442d7fde1d567037e1a686d56c9cd))
* Add option for P256 curve in init function while keeping old curve as default ([`50e691d`](https://github.com/evervault/evervault-python/commit/50e691d6fa2fbfeeca98b2c3efe968ec1a5cce3b))
* Add option for P256 curve in init function while keeping old curve as default ([`1200a80`](https://github.com/evervault/evervault-python/commit/1200a80ccfb8dea24f7b5bbc1230124b760b5080))
* Add option for P256 curve in init function while keeping old curve as default ([`9585c6c`](https://github.com/evervault/evervault-python/commit/9585c6c2a7102a227a7170e95822b14a874943ab))
* Add option for P256 curve in init function while keeping old curve as default ([`1549674`](https://github.com/evervault/evervault-python/commit/15496746ee93ab57b214ef5af1f68695ba5485cb))
* Add option for P256 curve in init function while keeping old curve as default ([`35f7fb1`](https://github.com/evervault/evervault-python/commit/35f7fb1b3fc5e56731e0eee8263b40379fa291e2))
* Add option for P256 curve in init function while keeping old curve as default ([`a1293f8`](https://github.com/evervault/evervault-python/commit/a1293f8559921c8d99050a9292ed0f1941bd6a3f))
* Add option for P256 curve in init function while keeping old curve as default ([`2e1eb01`](https://github.com/evervault/evervault-python/commit/2e1eb016b54c8d7ac013d39f7f7738160e937b21))
* Add option for P256 curve in init function while keeping old curve as default ([`57b8c07`](https://github.com/evervault/evervault-python/commit/57b8c0756c379cd0c7ae63b46d8fba0ba7117f7f))
* Add option for P256 curve in init function while keeping old curve as default ([`b12695a`](https://github.com/evervault/evervault-python/commit/b12695adee549eec3ce772a8d6b99f59f76636b2))
* Add option for P256 curve in init function while keeping old curve as default ([`5ceecaf`](https://github.com/evervault/evervault-python/commit/5ceecaf8cca98ac0fd3e465805b7fb5147185c88))
* Add optional retries to requests for cert and cage operations ([`5c28881`](https://github.com/evervault/evervault-python/commit/5c288811c5e51cd5621d24e90d236b6c0607ffbb))
* Batch send encryption metrics ([`4975eba`](https://github.com/evervault/evervault-python/commit/4975eba1344d8347868be60f5c4a118e5f7fca84))

### Fix
* Remove cert check code as it is non functional ([`a573650`](https://github.com/evervault/evervault-python/commit/a57365055187493e3cfe3abdafda4e77d2cc0a81))
* Assert certificate presence when relay is called ([`e87dac5`](https://github.com/evervault/evervault-python/commit/e87dac580fbac3b9c3029b1cb17e9477dc6c6dab))
* **error handling:** Add support for forbidden IP responses ([`66ddfd5`](https://github.com/evervault/evervault-python/commit/66ddfd5fbf8bcac8d24e753557cce4aaa7cdcb89))
* **docs:** Include reference to commitizen and contributing.md ([`a5f626a`](https://github.com/evervault/evervault-python/commit/a5f626a796ce0bf65212f1225810123410626608))
* Release new runtime error support ([`7018d75`](https://github.com/evervault/evervault-python/commit/7018d75f2af335e989b55531f33b7a66fa7991de))
* **docs:** Update example to include retry ([`8dd9ec7`](https://github.com/evervault/evervault-python/commit/8dd9ec736c5ec5379bec8004a046f102f8b4be41))
* **actions:** Add access token to checkout ([`6004937`](https://github.com/evervault/evervault-python/commit/600493748380a38dc69abd6511c1b2fccfaea170))
* Avoid posting empty metrics ([`06fc26b`](https://github.com/evervault/evervault-python/commit/06fc26b70d99e91ad3c61e93a952159b84bb8afb))
* Non-blocking metrics reporting ([`8449e30`](https://github.com/evervault/evervault-python/commit/8449e302d246d3d9c20546053d0e80c62f2a2641))

### Documentation
* **contributing:** Add a CONTRIBUTING.md and checklist ([`05ac094`](https://github.com/evervault/evervault-python/commit/05ac094c240ec784118c365884889f744f85b120))
* Clean out old contributing code ([`98ed284`](https://github.com/evervault/evervault-python/commit/98ed2846219f32bf3dad201efef915af72313b8d))

## v0.7.1 (2022-03-30)
### Fix
* Assert certificate presence when relay is called ([`e87dac5`](https://github.com/evervault/evervault-python/commit/e87dac580fbac3b9c3029b1cb17e9477dc6c6dab))

## v0.7.0 (2022-03-16)
### Feature
* Implement latest crypto scheme support adding KDF to derived secret keys ([`f7c5e49`](https://github.com/evervault/evervault-python/commit/f7c5e496508b0b31f570b14e8bffb4c2fccb2e77))

## v0.6.0 (2022-02-03)
### Feature
* Add option for P256 curve in init function while keeping old curve as default ([`98b709c`](https://github.com/evervault/evervault-python/commit/98b709ca39f442d7fde1d567037e1a686d56c9cd))
* Add option for P256 curve in init function while keeping old curve as default ([`50e691d`](https://github.com/evervault/evervault-python/commit/50e691d6fa2fbfeeca98b2c3efe968ec1a5cce3b))
* Add option for P256 curve in init function while keeping old curve as default ([`1200a80`](https://github.com/evervault/evervault-python/commit/1200a80ccfb8dea24f7b5bbc1230124b760b5080))
* Add option for P256 curve in init function while keeping old curve as default ([`9585c6c`](https://github.com/evervault/evervault-python/commit/9585c6c2a7102a227a7170e95822b14a874943ab))
* Add option for P256 curve in init function while keeping old curve as default ([`1549674`](https://github.com/evervault/evervault-python/commit/15496746ee93ab57b214ef5af1f68695ba5485cb))
* Add option for P256 curve in init function while keeping old curve as default ([`35f7fb1`](https://github.com/evervault/evervault-python/commit/35f7fb1b3fc5e56731e0eee8263b40379fa291e2))
* Add option for P256 curve in init function while keeping old curve as default ([`a1293f8`](https://github.com/evervault/evervault-python/commit/a1293f8559921c8d99050a9292ed0f1941bd6a3f))
* Add option for P256 curve in init function while keeping old curve as default ([`2e1eb01`](https://github.com/evervault/evervault-python/commit/2e1eb016b54c8d7ac013d39f7f7738160e937b21))
* Add option for P256 curve in init function while keeping old curve as default ([`57b8c07`](https://github.com/evervault/evervault-python/commit/57b8c0756c379cd0c7ae63b46d8fba0ba7117f7f))
* Add option for P256 curve in init function while keeping old curve as default ([`b12695a`](https://github.com/evervault/evervault-python/commit/b12695adee549eec3ce772a8d6b99f59f76636b2))
* Add option for P256 curve in init function while keeping old curve as default ([`5ceecaf`](https://github.com/evervault/evervault-python/commit/5ceecaf8cca98ac0fd3e465805b7fb5147185c88))

## v0.5.0 (2022-01-31)
### Feature
* Add optional retries to requests for cert and cage operations ([`5c28881`](https://github.com/evervault/evervault-python/commit/5c288811c5e51cd5621d24e90d236b6c0607ffbb))
* Batch send encryption metrics ([`4975eba`](https://github.com/evervault/evervault-python/commit/4975eba1344d8347868be60f5c4a118e5f7fca84))

### Fix
* **error handling:** Add support for forbidden IP responses ([`66ddfd5`](https://github.com/evervault/evervault-python/commit/66ddfd5fbf8bcac8d24e753557cce4aaa7cdcb89))
* **docs:** Include reference to commitizen and contributing.md ([`a5f626a`](https://github.com/evervault/evervault-python/commit/a5f626a796ce0bf65212f1225810123410626608))
* Release new runtime error support ([`7018d75`](https://github.com/evervault/evervault-python/commit/7018d75f2af335e989b55531f33b7a66fa7991de))
* **docs:** Update example to include retry ([`8dd9ec7`](https://github.com/evervault/evervault-python/commit/8dd9ec736c5ec5379bec8004a046f102f8b4be41))
* **actions:** Add access token to checkout ([`6004937`](https://github.com/evervault/evervault-python/commit/600493748380a38dc69abd6511c1b2fccfaea170))
* Avoid posting empty metrics ([`06fc26b`](https://github.com/evervault/evervault-python/commit/06fc26b70d99e91ad3c61e93a952159b84bb8afb))
* Non-blocking metrics reporting ([`8449e30`](https://github.com/evervault/evervault-python/commit/8449e302d246d3d9c20546053d0e80c62f2a2641))

### Documentation
* **contributing:** Add a CONTRIBUTING.md and checklist ([`05ac094`](https://github.com/evervault/evervault-python/commit/05ac094c240ec784118c365884889f744f85b120))
* Clean out old contributing code ([`98ed284`](https://github.com/evervault/evervault-python/commit/98ed2846219f32bf3dad201efef915af72313b8d))

## v0.4.3 (2022-01-11)
### Fix
* **docs:** Include reference to commitizen and contributing.md ([`a5f626a`](https://github.com/evervault/evervault-python/commit/a5f626a796ce0bf65212f1225810123410626608))

## v0.4.2 (2022-01-10)
### Fix
* Release new runtime error support ([`7018d75`](https://github.com/evervault/evervault-python/commit/7018d75f2af335e989b55531f33b7a66fa7991de))

## v0.4.1 (2021-12-15)
### Fix
* **docs:** Update example to include retry ([`8dd9ec7`](https://github.com/evervault/evervault-python/commit/8dd9ec736c5ec5379bec8004a046f102f8b4be41))

## v0.4.0 (2021-12-03)
### Feature
* Add optional retries to requests for cert and cage operations ([`5c28881`](https://github.com/evervault/evervault-python/commit/5c288811c5e51cd5621d24e90d236b6c0607ffbb))

### Fix
* **actions:** Add access token to checkout ([`6004937`](https://github.com/evervault/evervault-python/commit/600493748380a38dc69abd6511c1b2fccfaea170))

### Documentation
* **contributing:** Add a CONTRIBUTING.md and checklist ([`05ac094`](https://github.com/evervault/evervault-python/commit/05ac094c240ec784118c365884889f744f85b120))

## v0.3.0 (2021-09-20)
### Feature
* Batch send encryption metrics ([`4975eba`](https://github.com/evervault/evervault-python/commit/4975eba1344d8347868be60f5c4a118e5f7fca84))

### Fix
* Avoid posting empty metrics ([`06fc26b`](https://github.com/evervault/evervault-python/commit/06fc26b70d99e91ad3c61e93a952159b84bb8afb))
* Non-blocking metrics reporting ([`8449e30`](https://github.com/evervault/evervault-python/commit/8449e302d246d3d9c20546053d0e80c62f2a2641))

### Documentation
* Clean out old contributing code ([`98ed284`](https://github.com/evervault/evervault-python/commit/98ed2846219f32bf3dad201efef915af72313b8d))

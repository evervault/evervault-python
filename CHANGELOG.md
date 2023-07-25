# CHANGELOG



## v3.0.0 (2023-07-21)

### Breaking

* feat!: Release decrypt function

BREAKING CHANGE: The ID of the App is now required when initialising the SDK ([`c3e474c`](https://github.com/evervault/evervault-python/commit/c3e474c5415c00db567914436c33fbdccb2ed077))

* feat!: Release decrypt function ([`02b292b`](https://github.com/evervault/evervault-python/commit/02b292bd276492ff1341c6f882cbf15562bbe907))

* feat!: Require App UUID when initialising the SDK

BREAKING CHANGE: The UUID of the App is now required when initialising the SDK ([`ead3a76`](https://github.com/evervault/evervault-python/commit/ead3a760d9caa94a2a25ae3ee9b1d4101b24e30e))

### Ci

* ci: fix tests workflow (#91)

* trigger test action

* try use local setup

* try just bumping poetry

* fix tests

* lint ([`b23fc2c`](https://github.com/evervault/evervault-python/commit/b23fc2c8be822d146e242ef63e035e2f7b4217d2))

### Feature

* feat(cages attestation): allow users to pass in a list of sets of PCRs for attesting their Cages (#92)

* pass list of PCRs to the attestation bindings

* bump attestation version

* document ([`20ed2a6`](https://github.com/evervault/evervault-python/commit/20ed2a60493e92473793114cc6be4c1019e4b515))

* feat: add crc32 to encrypted files ([`0467c5d`](https://github.com/evervault/evervault-python/commit/0467c5d0e1273ed7e35ac219e896caa631c9f5f2))

### Fix

* fix: dont use debug keys ([`025fdd1`](https://github.com/evervault/evervault-python/commit/025fdd1de2424e920e678611cebc424722e612cb))

### Unknown

* Merge pull request #102 from evervault/jake/poetry-bump

feat!: Release decrypt function ([`cf31c58`](https://github.com/evervault/evervault-python/commit/cf31c585ae57c810dd258e6b6944868cb573586d))

* Merge pull request #93 from evervault/jake/etr-815-update-sdk-to-be-initd-using-app-uuid

feat!: Require App UUID when initialising the SDK ([`2a1a03a`](https://github.com/evervault/evervault-python/commit/2a1a03ab0318b372c036114cffae4183819ce711))

* update readme ([`db038f8`](https://github.com/evervault/evervault-python/commit/db038f84cc8b942f46dd9bd883d2da8b1bff3d0c))

* Fixes boolean encryption ([`dbf579a`](https://github.com/evervault/evervault-python/commit/dbf579a2abd993026121baa536d715194293c5aa))

* formatting code ([`32213fb`](https://github.com/evervault/evervault-python/commit/32213fbccfb02277a68106dc0516e8080e26db74))

* Add various improvements ([`235c896`](https://github.com/evervault/evervault-python/commit/235c896bde079a89817bb358d877955bc3ceb65e))

* fmt ([`b5ea9a9`](https://github.com/evervault/evervault-python/commit/b5ea9a92b570300da512e1d80193b280cff7b83e))

* reorder app id ([`a183884`](https://github.com/evervault/evervault-python/commit/a183884d45825a4dff0a7de2ac15a74f2a063176))

* only include auth basic header on decrypt route ([`c9558ed`](https://github.com/evervault/evervault-python/commit/c9558ed34dd9708c0ca4e4ae3bd9e6196f3292c6))

* Doc changes ([`5e696a4`](https://github.com/evervault/evervault-python/commit/5e696a4138636dc498bf11bccc7c88258c89522a))

* clean up ([`6bcb1b8`](https://github.com/evervault/evervault-python/commit/6bcb1b83534dd4da6cea67da9c08745279470aa1))

* Support byte responses ([`556da8c`](https://github.com/evervault/evervault-python/commit/556da8cde90267e8a8d11cf45377a4f62fb13e3e))

* Merge pull request #95 from evervault/chinaza/downgrade-poetry-lockfile

Downgrade poetry lockfile ([`06ed1a6`](https://github.com/evervault/evervault-python/commit/06ed1a6b458efa295147b0ce5d1b4b32cc40cc71))

* Downgrade poetry lockfile ([`75c7764`](https://github.com/evervault/evervault-python/commit/75c7764808203be8ab874ec8a3d402350f24efc9))

* Update flake8 version ([`79075f1`](https://github.com/evervault/evervault-python/commit/79075f104f22dc908ee0095148dff4071eb8caed))

* Update poetry python version ([`0cd35f6`](https://github.com/evervault/evervault-python/commit/0cd35f6a2eb76d9423c766a043c35ad66a38de79))

* Update poetry python version ([`46c5781`](https://github.com/evervault/evervault-python/commit/46c5781a7d1251d50c141734c52589a074ba36f7))

* Update black version ([`99ed80d`](https://github.com/evervault/evervault-python/commit/99ed80dd12f39cbcd00eefe4e6017f8d6d52b64c))

* Merge pull request #94 from evervault/cian/depbot-crypto

Dependabot requires lock file present for it to create PRs for patches ([`4c69151`](https://github.com/evervault/evervault-python/commit/4c69151a329782b6cae177d68e2eb48dcfa92e04))

* update cryptography version and min python version ([`fc58d96`](https://github.com/evervault/evervault-python/commit/fc58d96af9a34131e11eba6990af7e3172f58ab3))

* Dependabot requires lock file present for it to create PRs for patches ([`450666a`](https://github.com/evervault/evervault-python/commit/450666a4a3e531ba84640723012f5f224054e5b1))

* format ([`612da5f`](https://github.com/evervault/evervault-python/commit/612da5fc292fce94a3c15df7f0216bb0024763bb))

* Add decrypt function ([`5030147`](https://github.com/evervault/evervault-python/commit/50301475b6fd75706a8426b74a2be10e630268d6))

* keep Api-Key header for compatibility ([`b44b0ce`](https://github.com/evervault/evervault-python/commit/b44b0cee159cd7d7223b6c04bd723c6ec9c302a6))

* Merge pull request #90 from evervault/eoinpm/pro-2038-update-python-sdk-to-add-new-crc-bytes

Update Python SDK to add CRC32 checksum ([`683331c`](https://github.com/evervault/evervault-python/commit/683331c2fffc6c0abf7b78c11b834e5d1aae1027))


## v2.2.0 (2023-03-14)

### Chore

* chore: renaming test ([`0ac29d6`](https://github.com/evervault/evervault-python/commit/0ac29d67f1fe472105cbfedb98a22d7677773898))

### Feature

* feat: throw error on file size too large ([`c9ce0ce`](https://github.com/evervault/evervault-python/commit/c9ce0ce204c6705bfda1eb99ad1f24ae5d9707d1))

### Fix

* fix: allow encryption of bytearrays ([`1e43f52`](https://github.com/evervault/evervault-python/commit/1e43f52488a97a0b4e04635259de0e02ded2ab07))

### Unknown

* Merge pull request #89 from evervault/deirdre/pro-2031-enforce-file-size-limit-in-python-sdk

feat: throw error on file size too large ([`1e2f8ba`](https://github.com/evervault/evervault-python/commit/1e2f8bac72aa04833bdad2a9173ded037cc271d0))

* Merge pull request #88 from evervault/deirdre/pro-2033-bytearray-is-not-handled-in-python-sdk

fix: allow encryption of bytearrays ([`7e785c9`](https://github.com/evervault/evervault-python/commit/7e785c9b99c01f2ad9463bcdd452128461b221be))


## v2.1.1 (2023-02-21)

### Fix

* fix(create_run_token): provide default value for data argument ([`6e9200b`](https://github.com/evervault/evervault-python/commit/6e9200b1daffa813d49c1f3045f585862597fbe8))

### Unknown

* Merge pull request #87 from evervault/jake/hotfix-run-token-create

fix(create_run_token): provide default value for data argument ([`ea3f321`](https://github.com/evervault/evervault-python/commit/ea3f3218e7e71b40cb76f4edd756e2e26503cc58))


## v2.1.0 (2023-02-21)

### Feature

* feat: allow non preapproved payloads for run tokens ([`4430366`](https://github.com/evervault/evervault-python/commit/4430366a0b78a8aba2800670b0b76193ebc74aba))

### Unknown

* Merge pull request #86 from evervault/jake/etr-572-convert-none-type-payloads-to-empty

feat: allow non preapproved payloads for run tokens ([`c717141`](https://github.com/evervault/evervault-python/commit/c717141c06647458bb02c832442d12a3839bf8ab))

* Convert None type payloads to empty dictionary when creating run tokens ([`07e7bba`](https://github.com/evervault/evervault-python/commit/07e7bbaa5bfd2d39fd17b2dc7466b8967a9ed9bd))


## v2.0.0 (2023-02-15)

### Breaking

* fix!: Update version of cryptography dependency to remove soundness vulnerability. BREAKING CHANGE: removes support for OpenSSL &lt; 1.1.0, LibreSSL &lt; 3.5, macOS &lt; 10.12 ([`bbaf58c`](https://github.com/evervault/evervault-python/commit/bbaf58c962ff9780e8573b9577bd08343c865d17))

### Chore

* chore: upadte readme with cage_requests_session ([`5e01545`](https://github.com/evervault/evervault-python/commit/5e015455ea6c25fc940c9a90b213c51ebc82c5be))

### Unknown

* Merge pull request #85 from evervault/fix/update-cryptography-dependency

fix!: update cryptography dependency to remove vuln ([`d74f160`](https://github.com/evervault/evervault-python/commit/d74f160177ef57073d4cec37d31b7be981a24187))

* Merge pull request #84 from evervault/chore/update-readme

Update readme with cage requests session info ([`3770472`](https://github.com/evervault/evervault-python/commit/3770472c1dbdab1c4b5a9f787add47ea5945e237))


## v1.7.0 (2023-02-09)

### Feature

* feat(cages): introduce support for cage attestation by exposing a cage request session builder ([`256d78c`](https://github.com/evervault/evervault-python/commit/256d78ccf667a4637ca96fd9316260a12854848a))

### Style

* style: format again ([`cb5d82c`](https://github.com/evervault/evervault-python/commit/cb5d82c54789b0c31f15a045e40f8ab71272d83a))

* style: resolve disagreement between formatters ([`2d75f0f`](https://github.com/evervault/evervault-python/commit/2d75f0fba03ceb9ec84e91d66a75cb29d7af2c05))

* style: remove whitespace in slice index ([`9b70fe6`](https://github.com/evervault/evervault-python/commit/9b70fe6a95914001dafec5eecbf4806e6bca75ca))

* style: format cage client ([`2e296d7`](https://github.com/evervault/evervault-python/commit/2e296d708c83588693e3c350e830cd78c7d88f75))

### Unknown

* Merge pull request #83 from evervault/david/spe-317-add-client-to-python-sdk-for-making

Add Cages client to python sdk for attesting connections ([`2cae802`](https://github.com/evervault/evervault-python/commit/2cae802c16d77be8d8f78d8b62739b2e0452fead))


## v1.6.0 (2023-02-03)

### Chore

* chore: run black ([`3446c33`](https://github.com/evervault/evervault-python/commit/3446c33e901b757c854244b2fe5f3c9881e95833))

* chore: run black ([`306c454`](https://github.com/evervault/evervault-python/commit/306c454f07d917853c49fb4fdfd446fe9c61257a))

* chore: run black ([`7457d99`](https://github.com/evervault/evervault-python/commit/7457d9978c32f902d559e598cc68289459f0a977))

### Feature

* feat: support file encryption ([`42ac534`](https://github.com/evervault/evervault-python/commit/42ac53427f903c7344f2329e1705aa5816bd927f))

### Test

* test: add file encryption tests ([`2325196`](https://github.com/evervault/evervault-python/commit/232519621d05db6b351df65783942f34ad9abe41))

### Unknown

* Merge pull request #82 from evervault/eoinpm/pro-1872-python-sdk-support

feat: support file encryption ([`c2bce7f`](https://github.com/evervault/evervault-python/commit/c2bce7f33cd35b28c9d1aef5d93ac8c0dba3eec6))

* Revert &#34;chore: run black&#34;

This reverts commit 306c454f07d917853c49fb4fdfd446fe9c61257a. ([`ecc7a2d`](https://github.com/evervault/evervault-python/commit/ecc7a2da0ebd97cba40895a4e2ef859800d06dec))

* Merge branch &#39;master&#39; of github.com:evervault/evervault-python into eoinpm/pro-1872-python-sdk-support ([`fb88369`](https://github.com/evervault/evervault-python/commit/fb883698468fdf4076a23a70616d6899f931cb83))


## v1.5.0 (2022-12-22)

### Chore

* chore: lints ([`0d7ce35`](https://github.com/evervault/evervault-python/commit/0d7ce353306f1535734f5ffbd8ac13d70c6959c1))

* chore: linted files ([`aa1ecdb`](https://github.com/evervault/evervault-python/commit/aa1ecdbbdfd7883901855c956b3c2edb786f38f9))

### Documentation

* docs: fix link in table ([`a8345f1`](https://github.com/evervault/evervault-python/commit/a8345f1d792b5553403dfc2bdac3dbb00d27c18a))

* docs: mention async python in readme ([`c3f94ef`](https://github.com/evervault/evervault-python/commit/c3f94efde4d2a493104ba114bab055a44d2476d7))

### Feature

* feat: support aiohttp requests for outbound relay ([`a059aa7`](https://github.com/evervault/evervault-python/commit/a059aa7dcb58759b24ca1eabd10f2da0262c01fb))

### Fix

* fix: remove erroneously included debug print ([`41ce243`](https://github.com/evervault/evervault-python/commit/41ce243296807225a4b2ce61d55545a96a2f4f41))

### Unknown

* Merge pull request #81 from evervault/eoinpm/python-async-oubound-requests

Support aiohttp async requests in Python ([`21ede3a`](https://github.com/evervault/evervault-python/commit/21ede3afd3ad05cd8a14191376101cb86df97633))


## v1.4.0 (2022-12-14)

### Feature

* feat: Increase frequency at which the Outbound Relay Config cache is refreshed (#80)

* Fixes timer

* Various improvements

* Various improvements

* attempt at fixing tests

* Reformat code

* Minor improvement ([`3d05c58`](https://github.com/evervault/evervault-python/commit/3d05c58d1878b8adc837afc8ade81f7ef926c9bf))


## v1.3.3 (2022-11-16)

### Fix

* fix: remove decryption domains from whitelist (#79) ([`d5af814`](https://github.com/evervault/evervault-python/commit/d5af81443bdd527376af28c7ad2214b5ec6c0157))

### Unknown

* Create codeql.yml ([`0b9079c`](https://github.com/evervault/evervault-python/commit/0b9079c7e8f605013c6b3baeeabcf51c1dba94a8))


## v1.3.2 (2022-11-07)

### Fix

* fix: Replace recursive timer call with RepeatedTimer class (#78) ([`cf22d6c`](https://github.com/evervault/evervault-python/commit/cf22d6c0e8c352d6228497efd0f4e8babdff0769))


## v1.3.1 (2022-11-04)

### Fix

* fix: store thread spawing on each call to init (#77) ([`e5ae0e1`](https://github.com/evervault/evervault-python/commit/e5ae0e1ef3fbb750cc8dc7bb396fd022e18c8603))

### Unknown

* Revert &#34;Fix: Don&#39;t spawn thread in loop (#75)&#34; (#76)

This reverts commit d195dea345e1720b1c22318c53c168fd6a46bc2e. ([`4d38878`](https://github.com/evervault/evervault-python/commit/4d38878c869336917b0416b68bd0352d8d7e3251))

* Fix: Don&#39;t spawn thread in loop (#75)

* Add new Repeater timer class

* fix: refactor the repeated command

* refactor: format code

* refactor: remove import ([`d195dea`](https://github.com/evervault/evervault-python/commit/d195dea345e1720b1c22318c53c168fd6a46bc2e))


## v1.3.0 (2022-10-27)

### Feature

* feat: poll the Evervault API for relay outbound configuration (#74)

* feat: pull outbound relay config from the evervault api at an interval

* refactor: add error handling to relay config call

* refector: remove e2e test

* refactor: Format code ([`e1cbfb4`](https://github.com/evervault/evervault-python/commit/e1cbfb4694ee37140880cfb3b850c91be8a52f8b))

### Unknown

* Revert &#34;Pull relay config from API (#72)&#34; (#73)

This reverts commit 766944b3d81116331c12790a14a663d0dad47df3. ([`f2fea6b`](https://github.com/evervault/evervault-python/commit/f2fea6b9b4180308279a80976d1d0ec54d3503ba))

* Pull relay config from API (#72)

* feat: pull outbound relay config from the evervault api at an interval

* refactor: add error handling to relay config call

* refector: remove e2e test

* refactor: Format code ([`766944b`](https://github.com/evervault/evervault-python/commit/766944b3d81116331c12790a14a663d0dad47df3))


## v1.2.1 (2022-09-23)

### Chore

* chore(manifest): fixes typo in pyproject.toml description. ([`1a49868`](https://github.com/evervault/evervault-python/commit/1a498686e85d8bd85c4424df567d66ec952ac300))

### Fix

* fix: empty proxies for each request ([`8d9c6a2`](https://github.com/evervault/evervault-python/commit/8d9c6a2d536d98dacb295b4c4595a79f384ac499))

### Unknown

* Merge pull request #71 from evervault/eoinpm/fix-python-sdk-in-lambdas

fix: empty proxies for each request ([`b4e4508`](https://github.com/evervault/evervault-python/commit/b4e4508964e0a555a66042f6f885021f47b231aa))

* Merge pull request #70 from kamidzi/master

chore(manifest): fixes typo in pyproject.toml description. ([`ac59f8e`](https://github.com/evervault/evervault-python/commit/ac59f8e2f1dda72a60cb14d479f66345052c643d))


## v1.2.0 (2022-09-05)

### Documentation

* docs(createruntoken): describing run tokens ([`e8ee900`](https://github.com/evervault/evervault-python/commit/e8ee900f10d8ac61905fa89735db54b227ae3742))

### Feature

* feat(create_run_token): adding create_run_token ([`177236a`](https://github.com/evervault/evervault-python/commit/177236a944de99e9ea5278123a3e96e9a7b82c35))

### Test

* test(create_run_token): linting ([`723ab1f`](https://github.com/evervault/evervault-python/commit/723ab1f9ce6e901d1364edfae185fe035ff2596f))

* test(create_run_token): adding tests ([`d8069c3`](https://github.com/evervault/evervault-python/commit/d8069c3cc43871cc3c89a7cb9cdc57cd5bf8e461))

### Unknown

* Merge pull request #69 from evervault/deirdre/pro-1547-add-createruntoken-to-python-sdk

feat(create_run_token): adding create_run_token ([`48a462d`](https://github.com/evervault/evervault-python/commit/48a462d7dc9fd1acee75fceb998ff8f8ddaa7a15))


## v1.1.0 (2022-07-20)

### Documentation

* docs: Adds wildcard reference ([`5d7bfc7`](https://github.com/evervault/evervault-python/commit/5d7bfc7e440de2690beca949a2ff177758d704a3))

### Feature

* feat(outbound): Supports wildcard decryption domains ([`dbdf279`](https://github.com/evervault/evervault-python/commit/dbdf2796a6a9bbef43536186399daa0d1b658777))

### Unknown

* Merge pull request #68 from evervault/eoinpm/pro-1051-wildcard-decryptiondomains-in-python-sdk

feat(outbound): Supports wildcard decryption domains ([`c64a499`](https://github.com/evervault/evervault-python/commit/c64a499d30c1f545ec2ac24dc3d6afc624562b6f))


## v1.0.0 (2022-07-06)

### Breaking

* feat: Supports decrypt_domains config option

This is a breaking change

BREAKING CHANGE: Traffic won&#39;t be sent through outbound proxy by default anymore ([`1a69cce`](https://github.com/evervault/evervault-python/commit/1a69cce6254ba09d62510b2ff3adc9b8a2def22b))

### Unknown

* Merge pull request #66 from evervault/eoinpm/pro-969-update-python-sdk-to-use

feat!: supports decrypt_domains config option

BREAKING CHANGE: Changes the default outbound relay behaviour ([`53386d6`](https://github.com/evervault/evervault-python/commit/53386d688ab8630e559f29128d48e33b82e1ee57))

* Merge branch &#39;master&#39; into eoinpm/pro-969-update-python-sdk-to-use ([`92a53ff`](https://github.com/evervault/evervault-python/commit/92a53ff5c2afa6607d54f1cd1c42ddec6a96ab1a))

* Update README.md ([`0435f05`](https://github.com/evervault/evervault-python/commit/0435f05a6274fc4f8ba60e02ce768057fa7d5867))

* Add debug flag ([`23152f1`](https://github.com/evervault/evervault-python/commit/23152f16e9f33c776129ef4b26de5cd8c8e3fe16))

* Update warning ([`a275f68`](https://github.com/evervault/evervault-python/commit/a275f686ec0fc3157292a1433a1f18a421599b0f))

* Update README.md ([`47226df`](https://github.com/evervault/evervault-python/commit/47226df827f927f1214ee0a3948e9129b6ac6886))

* Linting ([`00fff03`](https://github.com/evervault/evervault-python/commit/00fff031698ec90cfe22c594976887514ea5236a))

* The VSCode Python debugger is a godsend ([`30371b7`](https://github.com/evervault/evervault-python/commit/30371b7cb4a708bec5a2ab508c164e98a92e35a3))


## v0.8.4 (2022-06-30)

### Fix

* fix: Merge pull request #67 from evervault/eoinpm/pro-989-end-the-ddos-machine-python-sdk

fix: keeps static link to requests.Session.request ([`06d0d05`](https://github.com/evervault/evervault-python/commit/06d0d05bca35b9e4f19568e4d9087dff2c296b25))

* fix: keeps static link to requests.Session.request ([`65a281c`](https://github.com/evervault/evervault-python/commit/65a281c0cab89df19d8f40e22aab9bb519f75eb9))


## v0.8.3 (2022-06-29)

### Fix

* fix: respect ignore domains list ([`6fd9e49`](https://github.com/evervault/evervault-python/commit/6fd9e49051ba6c0ab016b0b4c38d4d92d86380b2))

### Unknown

* Merge pull request #65 from evervault/hannah/fix-ignore-domain

fix: respect ignore domains list ([`b83bce4`](https://github.com/evervault/evervault-python/commit/b83bce48868c9ccc3817631acf094e6b1a7c10eb))

* Merge pull request #64 from evervault/revert-63-hannah/fix-request-interception

Revert &#34;Fix: Respect ignore domains list&#34; ([`dd5a43c`](https://github.com/evervault/evervault-python/commit/dd5a43cd0f287532b4a787040348ddb5a9eda034))

* Revert &#34;Fix: Respect ignore domains list&#34; ([`76162e2`](https://github.com/evervault/evervault-python/commit/76162e2df81ed8b701915510ee4d3c890731b10c))

* Merge pull request #63 from evervault/hannah/fix-request-interception

Fix: Respect ignore domains list ([`2aa61d0`](https://github.com/evervault/evervault-python/commit/2aa61d08a153a96a6864d123ee9324782d9c2835))

* Add tests ([`1e330b9`](https://github.com/evervault/evervault-python/commit/1e330b92897268ba5b9b92711f46d6fafc3d7e06))

* Don&#39;t pass client self ([`22af419`](https://github.com/evervault/evervault-python/commit/22af41933c2a3efe043a49d4203e5cc688b292ca))

* Fix linter ([`81c5ae0`](https://github.com/evervault/evervault-python/commit/81c5ae0eb9a64e94718a711903d1f0efaa7904c6))

* Fix: Respect ignore domains list ([`6c59ad3`](https://github.com/evervault/evervault-python/commit/6c59ad36b481ff1cfd7167ce0dda5ee848f9b8a1))


## v0.8.2 (2022-05-12)

### Fix

* fix: format ([`e3010a9`](https://github.com/evervault/evervault-python/commit/e3010a961c26a9d8c0804e1e6a377e1816258ad0))

* fix: remove metrics ([`ade1ff9`](https://github.com/evervault/evervault-python/commit/ade1ff9ddfad9d231cbd8c4d83d33d609c0ba42a))

### Unknown

* Merge pull request #62 from evervault/eoin/remove-metrics-telemetry

fix: remove metrics ([`ca9ba71`](https://github.com/evervault/evervault-python/commit/ca9ba71a1f72c9557aaceb6d6038238c47846427))


## v0.8.1 (2022-05-04)

### Fix

* fix(crypto client): Dont add AAD when using K1 curve ([`bcb5548`](https://github.com/evervault/evervault-python/commit/bcb5548a9b1f468f604e353155179a40943f044a))

### Unknown

* Merge pull request #60 from evervault/jake/pro-671-only-add-aad-during-encryption-on

fix(crypto client): Dont add AAD when using K1 curve ([`68ea89c`](https://github.com/evervault/evervault-python/commit/68ea89c82bc6806faf879347a666c28e4e7a34b3))

* Use curve var ([`1d1c062`](https://github.com/evervault/evervault-python/commit/1d1c062a9660a5829efd1f56a9d39106bbe103df))

* Revert &#34;just adding debuging info&#34;

This reverts commit b9455eadb4a870cdfbfe65c810f1e2035373491c. ([`c995f8b`](https://github.com/evervault/evervault-python/commit/c995f8b5a12b70a706ca4133ac618dc79839e962))

* Revert &#34;Adding SSL_CERT_DIR environment variable.&#34;

This reverts commit ab46eac384c1cd7a035b2f52fd78fd0ce9e165b7. ([`4be12b6`](https://github.com/evervault/evervault-python/commit/4be12b6b6afbc90d6b8d1e43ad35af96db25d6d7))

* Adding SSL_CERT_DIR environment variable. ([`ab46eac`](https://github.com/evervault/evervault-python/commit/ab46eac384c1cd7a035b2f52fd78fd0ce9e165b7))

* just adding debuging info ([`b9455ea`](https://github.com/evervault/evervault-python/commit/b9455eadb4a870cdfbfe65c810f1e2035373491c))

* remove workflow changes ([`161c538`](https://github.com/evervault/evervault-python/commit/161c53876b5cff20a36f9ecc288c308947c40414))

* remove integration test ([`38b9b26`](https://github.com/evervault/evervault-python/commit/38b9b268c088580e36b34bfbd0ea67004856b186))

* add env vars to workflow ([`bb85d74`](https://github.com/evervault/evervault-python/commit/bb85d74463f2033e1dfd6b5aed0a8ca150b79479))

* lint ([`398dad2`](https://github.com/evervault/evervault-python/commit/398dad26cf3e680edd4ff08fa7f9137c4fc407e4))

* Add integration tests ([`c4ee967`](https://github.com/evervault/evervault-python/commit/c4ee96789b0e84eced1a80b77169d640ac5c5c0d))


## v0.8.0 (2022-04-13)

### Fix

* fix: remove cert check code as it is non functional ([`a573650`](https://github.com/evervault/evervault-python/commit/a57365055187493e3cfe3abdafda4e77d2cc0a81))

### Unknown

* Merge pull request #59 from evervault/eoin/release-old-version-as-new

fix: remove code for cert check ([`4c4d1fb`](https://github.com/evervault/evervault-python/commit/4c4d1fbde07cd66f5e8fe4e8e5237d5ba856612b))

* Merge pull request #58 from evervault/revert-57-jhonny/ev-832-assure-the-sdk-does-not-make-a-call

Revert &#34;Jhonny/ev 832 assure the sdk does not make a call&#34; ([`ed27911`](https://github.com/evervault/evervault-python/commit/ed27911a6746eeb07a963a030bdb9c9ee04246ed))

* Revert &#34;Jhonny/ev 832 assure the sdk does not make a call&#34; ([`fc3fac4`](https://github.com/evervault/evervault-python/commit/fc3fac481b00b00a2d42d5ed8efbc0850b3bb180))


## v0.7.1 (2022-03-30)

### Fix

* fix: assert certificate presence when relay is called ([`e87dac5`](https://github.com/evervault/evervault-python/commit/e87dac580fbac3b9c3029b1cb17e9477dc6c6dab))

### Unknown

* Merge pull request #57 from evervault/jhonny/ev-832-assure-the-sdk-does-not-make-a-call

Jhonny/ev 832 assure the sdk does not make a call ([`b45de64`](https://github.com/evervault/evervault-python/commit/b45de64b7351a7e08f28fd9524faa71634360c0a))

* Small refactor ([`d5a0f11`](https://github.com/evervault/evervault-python/commit/d5a0f11f56c093d29ed7b6df7e23d22127a37ad9))

* Small refactor ([`c4a6770`](https://github.com/evervault/evervault-python/commit/c4a6770c0a3a528a2ccd0fa670a360780e929aa7))

* Removing unused variable. ([`e53358c`](https://github.com/evervault/evervault-python/commit/e53358cb365964d0bf35a57998ac28505706614c))

* As soon you call relay, you force puts, gets, deletes and posts to have a certificate presence assertion ([`2a8d8d0`](https://github.com/evervault/evervault-python/commit/2a8d8d0aee1053e2605d4480bb4027b7ac081487))

* Formatting code ([`acffddd`](https://github.com/evervault/evervault-python/commit/acffdddc1ab90bd44301a4484a7493b80b9c7e6d))

* Asserting certificate exists when using get/post/put/delete ([`deba9ad`](https://github.com/evervault/evervault-python/commit/deba9ad3621c0f001e1487f5f6bc0302285aaccb))


## v0.7.0 (2022-03-16)

### Chore

* chore: remove unused file ([`c18e4c7`](https://github.com/evervault/evervault-python/commit/c18e4c79eee386839b9f23308d7b9e059f86abf1))

* chore: remove unused ecdh key property on crypto client ([`9f6c80d`](https://github.com/evervault/evervault-python/commit/9f6c80db7caa3823d64ec21a10481d8a845f2bfc))

* chore: store decoded team key alongside ecdh key, pass to encrypt function ([`cb2f078`](https://github.com/evervault/evervault-python/commit/cb2f078bd4682aee7be7e7262e3f8966156e66cc))

### Feature

* feat: implement latest crypto scheme support adding KDF to derived secret keys ([`f7c5e49`](https://github.com/evervault/evervault-python/commit/f7c5e496508b0b31f570b14e8bffb4c2fccb2e77))

### Refactor

* refactor: isolate curves into a new module, add test for der encoding, make individual curve impl easier ([`10ca6a6`](https://github.com/evervault/evervault-python/commit/10ca6a60a175dddd5d43f0a9f70fb90d68ea73a5))

* refactor: remove unused import ([`2ddbe8a`](https://github.com/evervault/evervault-python/commit/2ddbe8a7a85f91aee1f54f5d28f2d7d06edfa913))

### Style

* style: run formatter ([`296379a`](https://github.com/evervault/evervault-python/commit/296379acbcc7c1ebd043c6e82af2ed6f5ea2c016))

* style: run black formatting ([`b6caa5e`](https://github.com/evervault/evervault-python/commit/b6caa5e98f64515240c37bb1ebffecca99d0d42f))

### Unknown

* Merge pull request #55 from evervault/liam/pro-495-add-support-for-der-encoding-in-python ([`bde8b09`](https://github.com/evervault/evervault-python/commit/bde8b09c29d3ac76c101d5d40db47409a5459e38))

* Merge pull request #54 from evervault/jhonny/pro-245-update-sdks-to-retry-loading-ca-on

Jhonny/pro 245 update sdks to retry loading ca on ([`65e5588`](https://github.com/evervault/evervault-python/commit/65e5588d884fc88168c47502117ecd04bfbd92ff))

* implement der encoding in python ([`8ea9264`](https://github.com/evervault/evervault-python/commit/8ea9264475bcf778f739ca762c703b22902c6f45))

* Fix: correct accept encoding header ([`96b54f3`](https://github.com/evervault/evervault-python/commit/96b54f3cec9faab178842fd4838b192590d8ccd7))

* Removing pyopenssl ([`30ab84e`](https://github.com/evervault/evervault-python/commit/30ab84e7045f590fa2d769816d9c3e8be2633a21))

* Removing cryptography since pyopenssl has it as a dependency. ([`85b440d`](https://github.com/evervault/evervault-python/commit/85b440d60e19ac38456e1e479cf742527b96d841))

* Deprecating python 3.6 ([`2385d9e`](https://github.com/evervault/evervault-python/commit/2385d9ebc8327b54b12ff28f8e21b2b4a8dcd135))

* run flake ([`68d2e31`](https://github.com/evervault/evervault-python/commit/68d2e319d3ac8fd89b8c3b70776111f97df4d149))

* Formatting files ([`a549bf5`](https://github.com/evervault/evervault-python/commit/a549bf5e14be2880bf3e6c2d05646a164459134e))

* Validating before date for certificates. ([`7a9348c`](https://github.com/evervault/evervault-python/commit/7a9348c074de706705f53d3eee64c9f4c12f7826))

* Renaming Cert to requestintercept ([`3b72c3b`](https://github.com/evervault/evervault-python/commit/3b72c3bc45ce3734183da038ec254ae6264a4fdd))

* Tests passing. ([`08f7956`](https://github.com/evervault/evervault-python/commit/08f7956895c71b21ec43a0b36a58960e0bb5139f))

* Tests for post, delete and put ([`5b374ff`](https://github.com/evervault/evervault-python/commit/5b374ff352441efb47f4accf9f7982a770dfafe1))

* Validating expire date working as expected ([`bde5ee4`](https://github.com/evervault/evervault-python/commit/bde5ee414a2130496d407e36b9d9858e06392751))

* working on validating certificate ([`853af1a`](https://github.com/evervault/evervault-python/commit/853af1ad02e19699cdd9c155705ae534fc88f517))

* Removing dependency. ([`3825f2a`](https://github.com/evervault/evervault-python/commit/3825f2a1c49a7942d279222a92bf84d2570686eb))

* adding new dependency in order to get the expiration date for certificates. ([`18acd00`](https://github.com/evervault/evervault-python/commit/18acd0035670911d6dafc046451849883ddc5040))

* updating cert when expired on gets ([`09ebab6`](https://github.com/evervault/evervault-python/commit/09ebab6a5c0a78f4aafb480bde552bf36f55e37c))

* tests fixed ([`3ea0ce8`](https://github.com/evervault/evervault-python/commit/3ea0ce8376f3fc0548c78d4df97196aa261a58fd))

* Fixing some tests. ([`d2ffc31`](https://github.com/evervault/evervault-python/commit/d2ffc31dfcf3b93a8b6c7acfeef60373c659645d))

* Trying to decouple a little bit. ([`0939074`](https://github.com/evervault/evervault-python/commit/09390747c19b1b1d3345661a02a98bde5c97cb83))

* Fixing http ([`68fdebb`](https://github.com/evervault/evervault-python/commit/68fdebb347c4e84091954f8663afd2152fb55af5))

* Trying to decouple a little bit. ([`241a221`](https://github.com/evervault/evervault-python/commit/241a221d27060ba06591e0b9a16a886c0bf070a3))

* Working on some simple test. ([`dd69b90`](https://github.com/evervault/evervault-python/commit/dd69b907c39b1bd9abcfcc8cdf752b21c5122ecd))


## v0.6.0 (2022-02-03)

### Feature

* feat: Add option for P256 curve in init function while keeping old curve as default ([`98b709c`](https://github.com/evervault/evervault-python/commit/98b709ca39f442d7fde1d567037e1a686d56c9cd))

* feat: Add option for P256 curve in init function while keeping old curve as default ([`50e691d`](https://github.com/evervault/evervault-python/commit/50e691d6fa2fbfeeca98b2c3efe968ec1a5cce3b))

* feat: Add option for P256 curve in init function while keeping old curve as default ([`1200a80`](https://github.com/evervault/evervault-python/commit/1200a80ccfb8dea24f7b5bbc1230124b760b5080))

* feat: add option for P256 curve in init function while keeping old curve as default ([`9585c6c`](https://github.com/evervault/evervault-python/commit/9585c6c2a7102a227a7170e95822b14a874943ab))

* feat: Add option for P256 curve in init function while keeping old curve as default ([`1549674`](https://github.com/evervault/evervault-python/commit/15496746ee93ab57b214ef5af1f68695ba5485cb))

* feat: Add option for P256 curve in init function while keeping old curve as default ([`35f7fb1`](https://github.com/evervault/evervault-python/commit/35f7fb1b3fc5e56731e0eee8263b40379fa291e2))

### Unknown

* Merge pull request #50 from evervault/jake/pro-284-python-sdk-p256-support

feat: Add option for P256 curve in init function while keeping old cu... ([`347fbc9`](https://github.com/evervault/evervault-python/commit/347fbc9eb9ef0ebef10edf1d3f2e31ca78b5383e))

* Merge pull request #52 from evervault/jhonny/ev-806-create-a-java-sdk

Adding license file ([`f28a68d`](https://github.com/evervault/evervault-python/commit/f28a68d6f99af270365ce76b9d7ae4707fa32f87))

* Changing company name ([`b3d5ce5`](https://github.com/evervault/evervault-python/commit/b3d5ce5c19502747c105db90c4e831ff869760ca))

* Adding license file ([`c3788a0`](https://github.com/evervault/evervault-python/commit/c3788a06ec3951235b554acfaf740d9e25dc7808))


## v0.5.0 (2022-01-31)

### Feature

* feat: Add option for P256 curve in init function while keeping old curve as default ([`a1293f8`](https://github.com/evervault/evervault-python/commit/a1293f8559921c8d99050a9292ed0f1941bd6a3f))

* feat: Add option for P256 curve in init function while keeping old curve as default ([`2e1eb01`](https://github.com/evervault/evervault-python/commit/2e1eb016b54c8d7ac013d39f7f7738160e937b21))

* feat: add option for P256 curve in init function while keeping old curve as default ([`57b8c07`](https://github.com/evervault/evervault-python/commit/57b8c0756c379cd0c7ae63b46d8fba0ba7117f7f))

* feat: Add option for P256 curve in init function while keeping old curve as default ([`b12695a`](https://github.com/evervault/evervault-python/commit/b12695adee549eec3ce772a8d6b99f59f76636b2))

* feat: Add option for P256 curve in init function while keeping old curve as default ([`5ceecaf`](https://github.com/evervault/evervault-python/commit/5ceecaf8cca98ac0fd3e465805b7fb5147185c88))

### Fix

* fix(error handling): add support for forbidden IP responses ([`66ddfd5`](https://github.com/evervault/evervault-python/commit/66ddfd5fbf8bcac8d24e753557cce4aaa7cdcb89))

### Unknown

* Merge pull request #51 from evervault/liam/pro-385-update-python-sdk-to-return-ip-whitelist ([`b4f5f1c`](https://github.com/evervault/evervault-python/commit/b4f5f1ca15ebcca33ecd40e40c0ed8591dec8bcb))

* reformat ([`fafce2d`](https://github.com/evervault/evervault-python/commit/fafce2db5795eed56a34d1b21aa70fb7c80d7377))

* add tests for forbidden IP error handling ([`c80276e`](https://github.com/evervault/evervault-python/commit/c80276eb6e0c222444ebad4c864db67026a05e33))

* format ([`af6fb83`](https://github.com/evervault/evervault-python/commit/af6fb831ec49bde4d333607bbb90367372a807a4))

* bump version ([`4029509`](https://github.com/evervault/evervault-python/commit/402950949ce79388a89e6c83e1414d9d123a7599))

* add error type for rejected IP address ([`cdc7878`](https://github.com/evervault/evervault-python/commit/cdc78780437c1fb623bd77de67de8a4b6d393921))


## v0.4.3 (2022-01-11)

### Fix

* fix(docs): include reference to commitizen and contributing.md ([`a5f626a`](https://github.com/evervault/evervault-python/commit/a5f626a796ce0bf65212f1225810123410626608))

### Unknown

* Merge pull request #49 from evervault/liam/pro-327-update-python-docs-to-direct-to ([`80bc82c`](https://github.com/evervault/evervault-python/commit/80bc82c5dd2ad8b6a097b7ee71654f58d61c742f))


## v0.4.2 (2022-01-10)

### Fix

* fix: release new runtime error support ([`7018d75`](https://github.com/evervault/evervault-python/commit/7018d75f2af335e989b55531f33b7a66fa7991de))

### Unknown

* Merge pull request #48 from evervault/liam/trigger-release ([`29b0f07`](https://github.com/evervault/evervault-python/commit/29b0f0708539e1a3a0cc6db0be7622c8b9fbecda))

* Merge pull request #47 from evervault/deirdre/pro-326-add-new-errors-to-python-sdk

Adding new cage errors 408 and 422 ([`2386a3d`](https://github.com/evervault/evervault-python/commit/2386a3dd24ef96df1d8f6f2fce20fd564d3ecb30))

* Adding new cage errors 408 and 422 ([`e272230`](https://github.com/evervault/evervault-python/commit/e272230689c8f341ed5a2c37c2cf85acb5cf0b4e))


## v0.4.1 (2021-12-15)

### Fix

* fix(docs): update example to include retry ([`8dd9ec7`](https://github.com/evervault/evervault-python/commit/8dd9ec736c5ec5379bec8004a046f102f8b4be41))

### Unknown

* Merge pull request #46 from evervault/update-readme-retry

fix(docs): update example to include retry ([`8a5df90`](https://github.com/evervault/evervault-python/commit/8a5df90681c87fd0011a6a214dff1de451d63474))

* Merge pull request #45 from evervault/jake/pro-246-update-sdk-docs-to-reflect-retries

Update docs to reflect retry option ([`cf65c81`](https://github.com/evervault/evervault-python/commit/cf65c81657bdbc9d34ca16a4dd32f20d24f1b4f1))

* Update README.md

Co-authored-by: Donal Tuohy &lt;donal@evervault.com&gt; ([`ddc5f5f`](https://github.com/evervault/evervault-python/commit/ddc5f5f1702456381923dc16a98eb5018d167a16))

* Update docs to reflect retry option ([`c2e0aa7`](https://github.com/evervault/evervault-python/commit/c2e0aa75ed6fc694e15f24d10347e46cba50fb4e))


## v0.4.0 (2021-12-03)

### Documentation

* docs(contributing): add a CONTRIBUTING.md and checklist ([`05ac094`](https://github.com/evervault/evervault-python/commit/05ac094c240ec784118c365884889f744f85b120))

### Feature

* feat: Add optional retries to requests for cert and cage operations ([`5c28881`](https://github.com/evervault/evervault-python/commit/5c288811c5e51cd5621d24e90d236b6c0607ffbb))

### Fix

* fix(actions): add access token to checkout ([`6004937`](https://github.com/evervault/evervault-python/commit/600493748380a38dc69abd6511c1b2fccfaea170))

### Unknown

* Merge pull request #44 from evervault/jake/fix-release-action

fix(actions): add access token to checkout ([`86efe10`](https://github.com/evervault/evervault-python/commit/86efe104694741b6bfd87dc0be8876cb559733a1))

* Merge pull request #43 from evervault/eoin/add-request-retry-to-ev-calls

feat: Add optional retries to requests for cert and cage operations ([`a96df30`](https://github.com/evervault/evervault-python/commit/a96df308bb2637520b91882d37d212aa9a5bd32c))

* Merge branch &#39;eoin/add-request-retry-to-ev-calls&#39; of github.com:evervault/evervault-python into eoin/add-request-retry-to-ev-calls ([`035a0b2`](https://github.com/evervault/evervault-python/commit/035a0b28450f683b8400b1994dfb88a21702d95f))

* format files ([`904f46f`](https://github.com/evervault/evervault-python/commit/904f46fd6bfa341d6eb220c3faae0f505bfe4493))

* Add retries for cert and cage requests ([`19caeae`](https://github.com/evervault/evervault-python/commit/19caeae2c6aa179453c2fe8da2a2407285862128))

* Pass on ([`a5311ea`](https://github.com/evervault/evervault-python/commit/a5311ea4508db7f094b4e6958424a83800eec60f))

* Merge pull request #42 from evervault/adam/contributing-docs

Add a `CONTRIBUTING.md` and checklist to the PR template ([`8e71a34`](https://github.com/evervault/evervault-python/commit/8e71a3495cfb4fe78dbde5456875566a41c5e838))


## v0.3.0 (2021-09-20)

### Build

* build: add semantic release ([`3012b99`](https://github.com/evervault/evervault-python/commit/3012b99dc488dc2e211cb2f661bd51603a1ef42d))

### Chore

* chore: remove unused logo ([`abf0443`](https://github.com/evervault/evervault-python/commit/abf0443f75eb33377496cfa99fd49992de3f1e9f))

### Documentation

* docs: clean out old contributing code ([`98ed284`](https://github.com/evervault/evervault-python/commit/98ed2846219f32bf3dad201efef915af72313b8d))

### Feature

* feat: batch send encryption metrics ([`4975eba`](https://github.com/evervault/evervault-python/commit/4975eba1344d8347868be60f5c4a118e5f7fca84))

### Fix

* fix: avoid posting empty metrics ([`06fc26b`](https://github.com/evervault/evervault-python/commit/06fc26b70d99e91ad3c61e93a952159b84bb8afb))

* fix: non-blocking metrics reporting ([`8449e30`](https://github.com/evervault/evervault-python/commit/8449e302d246d3d9c20546053d0e80c62f2a2641))

### Refactor

* refactor: use poetry instead of setup.py ([`5302b58`](https://github.com/evervault/evervault-python/commit/5302b58774c68f1cdc9141fa781d368308def664))

### Style

* style: run black formatter ([`b64d48a`](https://github.com/evervault/evervault-python/commit/b64d48ad8716d8c4019c0ea05a99404fc8588e32))

* style: add flake8 lint ([`97e234f`](https://github.com/evervault/evervault-python/commit/97e234fd3fd1e5bfa0f729d1cf74170070eea921))

* style: add black to format code ([`bb4b1f8`](https://github.com/evervault/evervault-python/commit/bb4b1f897aa2e29c9414acef62322d2ce7576fc7))

### Test

* test: mock metrics endpoints in tests ([`0d6e4dd`](https://github.com/evervault/evervault-python/commit/0d6e4dd119c2536e879d0cea82d81e303fb33d3e))

* test: make tests work with poetry ([`3cf6ca8`](https://github.com/evervault/evervault-python/commit/3cf6ca877eb35a15b51c2f76bc7becf517cdf229))

### Unknown

* Merge pull request #41 from evervault/adam/eng-1290

Add Encrypt Metrics Reporting ([`2c9ff0d`](https://github.com/evervault/evervault-python/commit/2c9ff0d7f5fd4deda5ca8c2ae57e5b3ec7bfdd80))

* Merge pull request #40 from evervault/adam/eng-1514-sdk-spring-clean-lintersrelease

Spring Clean (Linters/Release Actions/Formatting/Dependencies/Etc) ([`e8c7ea7`](https://github.com/evervault/evervault-python/commit/e8c7ea77fbea3191b59bfae4dbe0f47ac7e35a1d))

* Merge pull request #39 from evervault/arran/eng-1473-pass-api-endpoints-as-optional-params-to

Support overrides of evervault endpoints via env variables ([`32430db`](https://github.com/evervault/evervault-python/commit/32430db1a8e51f7eccec144705b4c92fc7bb0031))

* Support overrides of evervault endpoints via env variables ([`2371c72`](https://github.com/evervault/evervault-python/commit/2371c72b7ea95f760397a916717f8bbdb9b94923))

* Merge pull request #38 from evervault/adam/eng-1261-implement-retry-behaviour-for-calls-to

Retry getting the CA if it fails once ([`2c06c04`](https://github.com/evervault/evervault-python/commit/2c06c04ddc9dd42c38640af503cd374cd6b5b0ab))

* Typo ([`0644632`](https://github.com/evervault/evervault-python/commit/0644632890df3dd1346190cfe5ba30813ba86e8a))

* Retry on an error ([`8e33410`](https://github.com/evervault/evervault-python/commit/8e334102354aa02f630169799cb7b9908c44a024))

* encrypted_data -&gt; data in run() params (#36) ([`fe6202a`](https://github.com/evervault/evervault-python/commit/fe6202a1a43d95bda0e7a48791b38bfaef92d4b2))

* Merge pull request #35 from evervault/adam/eng-1257-include-caevervaultcom-in-ignore-domains

Stop `ca.evervault.com` from going through Relay ([`01e1e7a`](https://github.com/evervault/evervault-python/commit/01e1e7a0c419e1f4b96c605e1aa07d63b0cbdeac))

* Stop certificate authority from going through Relay ([`0265cab`](https://github.com/evervault/evervault-python/commit/0265cab1b87db3bc230c46e555bec4883ce9f01e))

* Merge pull request #34 from evervault/deirdre/removing-deprecated-endpoints

Removing deprecated endpoints from readme ([`dcf3c08`](https://github.com/evervault/evervault-python/commit/dcf3c087d1a6a9e6d0ea1af4f7ba5b9f553f83ab))

* Removing deprecated endpoints from readme ([`daad38d`](https://github.com/evervault/evervault-python/commit/daad38d7ee151dd47be89bfe33c3c7e30b1d2cd1))

* Merge pull request #33 from evervault/deirdre/correcting-encrypt-and-run-in-readme

Correcting encrypt_and_run method call in readme ([`880b95f`](https://github.com/evervault/evervault-python/commit/880b95f91a74e59749eecc0fbcc6cb0d7fb044a3))

* Correcting encrypt_and_run method call in readme ([`e626097`](https://github.com/evervault/evervault-python/commit/e62609730eae33b4f6b450631398d502e2113e5e))

* update version (#32) ([`755c33f`](https://github.com/evervault/evervault-python/commit/755c33f9561b00adad2dd8a539665986105bb933))

* return better error message when user doesn&#39;t enter API key (#31) ([`3c4c6ee`](https://github.com/evervault/evervault-python/commit/3c4c6eecfd6684466d04517b81e000b1ef62e9c8))

* start using evervault.init() and default outbound interception to ON (#30) ([`254ab38`](https://github.com/evervault/evervault-python/commit/254ab3898529b5c11c706470b5223c68b735becc))

* Merge pull request #29 from evervault/adam/prepare-for-deploy

Prepare for deploy ([`1ef3013`](https://github.com/evervault/evervault-python/commit/1ef3013503c32a78bda605b3206fb021e618dd3f))

* Prepare for deploy ([`c0c2a9e`](https://github.com/evervault/evervault-python/commit/c0c2a9e9c7a5798e42a3ebc7bd1fc024cc80b400))

* Merge pull request #28 from evervault/adam/eng-1114-fix-python-sdk-when-using-latest

Override proxy rebuild method to fix API key being removed from requests ([`e2313a7`](https://github.com/evervault/evervault-python/commit/e2313a70e58db56af4c39e35c2fb87232e74d388))

* Override proxy rebuild method to fix API key being removed from requests ([`68f4dad`](https://github.com/evervault/evervault-python/commit/68f4dad9ec34c08a5afdf032851e3b0c001673c9))

* Merge pull request #27 from evervault/deirdre/eng-1051-add-new-encrypted-string-format-to

Deirdre/eng 1051 add new encrypted string format to ([`fd56073`](https://github.com/evervault/evervault-python/commit/fd560731aa87ee2fa847c2571458a18d8773b401))

* Removing handling for empty ev version ([`590293e`](https://github.com/evervault/evervault-python/commit/590293ed13a781a4bfa73ca8a13d39e9ceb0e458))

* Adding first version (DUB) ([`43771ba`](https://github.com/evervault/evervault-python/commit/43771baa017318d3100535731e071c2f594ea4c4))

* Adding new encrypted string format to include version ([`4ded34a`](https://github.com/evervault/evervault-python/commit/4ded34a613c470a8038e33fe20c43edb1bbab699))

* Updating Python SDK docs link in README ([`8efd855`](https://github.com/evervault/evervault-python/commit/8efd855839a630621bbbe96c1039b758cb4b0e13))

* update cages url to run.evervault.com ([`287689b`](https://github.com/evervault/evervault-python/commit/287689b20fd2a933ab72d6be908ab56f55b6eea9))

* Merge pull request #22 from evervault/ed/ev-716-fix-evervault-logo-link

Fix Evervault logo link on README ([`1b94fce`](https://github.com/evervault/evervault-python/commit/1b94fce3dbbcbe6556dc42652e3ae46bcd695fc5))

* Merge pull request #25 from evervault/david/eng-651-python-sdk-dont-send-requests-to-cages

Dont send requests to cages through Relay (Python SDK) ([`c266e1f`](https://github.com/evervault/evervault-python/commit/c266e1fa4b23e4387fc93f749f293907aee9ce3f))

* dont send requests to cages through Relay ([`9c3bc4a`](https://github.com/evervault/evervault-python/commit/9c3bc4ac4cfb49e6e03f51e1470fa030be80211f))

* update cert install error message ([`7fce2d6`](https://github.com/evervault/evervault-python/commit/7fce2d63fe3de80edb168e5cdac2324500a825ae))

* append ev root to certifi trusted roots and store in temp file ([`c3dd1c2`](https://github.com/evervault/evervault-python/commit/c3dd1c28652bdc90916d46d90a5c5e5686e941fc))

* Fix Evervault logo link on README

Link was pointing to old welcome.evervault.com website. ([`64f8aa7`](https://github.com/evervault/evervault-python/commit/64f8aa7d27c357bd01b5437f177189880d4aa6e0))

* handle params passed in as None ([`d4bb073`](https://github.com/evervault/evervault-python/commit/d4bb0732ac6eff5b0d52b920e878d0cc577bc627))

* bump version ([`c2ca8ec`](https://github.com/evervault/evervault-python/commit/c2ca8ece81b5089d74d17c2c4e37612c93054042))

* add ability to give list of domains not to send through Outbound Relay (#19) ([`580d1ae`](https://github.com/evervault/evervault-python/commit/580d1aeffb39e3ddccda3963ae3b9fadc9084bcf))

* append cert for outbound Relay to Certifi trusted CAs file ([`0c46a7f`](https://github.com/evervault/evervault-python/commit/0c46a7f67961d93dc0a854179b1bae3e2ae099d7))

* pull cert from ca.evervault.com (#17) ([`111af63`](https://github.com/evervault/evervault-python/commit/111af63a1f9a40f89ece9ce0054d907a65f89f95))

* #636 Add outbound relay capability to python SDK (#16) ([`8eff886`](https://github.com/evervault/evervault-python/commit/8eff88624a017b2df2aea995386a8208e562d22a))

* Merge pull request #15 from evervault/eoin/bump-package-version

Bump package version ([`66a08c5`](https://github.com/evervault/evervault-python/commit/66a08c5a237aab14b2228c06e435aaab870ae47e))

* Bump package version ([`2095f40`](https://github.com/evervault/evervault-python/commit/2095f40682bae9ed9ebddf2fb78e7dddef6635b6))

* Merge pull request #14 from evervault/boilsquid/implement-v2-crypto-scheme

Boilsquid/implement v2 crypto scheme ([`0851d1d`](https://github.com/evervault/evervault-python/commit/0851d1d2af502844c3f313267d92e858af9435b1))

* Make key interval a constant ([`9b7b0b9`](https://github.com/evervault/evervault-python/commit/9b7b0b9a4809c45333ae5c8e8a85fe7176e6b404))

* Add interval check for key, if &gt; 15 seconds regen key ([`09a16b3`](https://github.com/evervault/evervault-python/commit/09a16b3bb74ab2f5d4e9cc5286f35b946ebaedc4))

* Throw execpiton is type passed in is not supported by sdk ([`a69a3d0`](https://github.com/evervault/evervault-python/commit/a69a3d06e9bec33db88435ae6504223421b1e76b))

* Update README with new encrypt types ([`b786fbf`](https://github.com/evervault/evervault-python/commit/b786fbfdc42cb3267a2ae904299dbf4f1a7c7358))

* Implement new v2 crypto scheme and remove v1 ([`8692b6a`](https://github.com/evervault/evervault-python/commit/8692b6a1c6f8341e67016f56c78b480140b9e4b1))

* Merge pull request #12 from evervault/d6t5-python-readme-changes

update python readme ([`13d271b`](https://github.com/evervault/evervault-python/commit/13d271b6da2f87f1a6675e90e42b9604870b2937))

* Update README.md ([`e7c0ec2`](https://github.com/evervault/evervault-python/commit/e7c0ec25ac1fcf04aa7c233d36b7260a27e2f537))

* Update README.md ([`1942d6c`](https://github.com/evervault/evervault-python/commit/1942d6c97424ca40d92ff10be397af98385e4628))

* Update Badge to use Markdown ([`c552bcd`](https://github.com/evervault/evervault-python/commit/c552bcd57e704d8aaad30d288b1afd0a96ef8a69))

* Update Logo on README.md ([`4c94b02`](https://github.com/evervault/evervault-python/commit/4c94b027b79156bfde9ef1744bba6b744265af48))

* update python readme

making python readme consistent with docs ([`cba2e11`](https://github.com/evervault/evervault-python/commit/cba2e11d07b0d724f607bb8e777c5935e414cb96))

* Merge pull request #11 from evervault/liam/ch2627/add-support-for-async-cage-runs-to-python

Add support for async Cage runs to python ([`364aa55`](https://github.com/evervault/evervault-python/commit/364aa55fcb0a2e9161bccfe562bed5c553128b95))

* fix syntax errors ([`972acf3`](https://github.com/evervault/evervault-python/commit/972acf34da94f20b06fad6b0cee6d52d9eb63899))

* Merge branch &#39;liam/ch2627/add-support-for-async-cage-runs-to-python&#39; of github.com:evervault/evervault-python into liam/ch2627/add-support-for-async-cage-runs-to-python ([`66fe62f`](https://github.com/evervault/evervault-python/commit/66fe62f280844616200b2a87ccf785cc1a313066))

* support custom headers in request ([`b3cec90`](https://github.com/evervault/evervault-python/commit/b3cec90b05d4de185db35e70aa24316e811beed0))

* capitalize Cage ([`83a1330`](https://github.com/evervault/evervault-python/commit/83a1330cccca0ec6b876f93d7dde4c35be1303a9))

* update gitignore and delete *.pyc ([`b78e41f`](https://github.com/evervault/evervault-python/commit/b78e41fa22fb47c6fdc7261a2a0d591b0cf999f4))

* more linting ([`3bbcd51`](https://github.com/evervault/evervault-python/commit/3bbcd51f599e12c3a1029811b3ccdb90963c8868))

* linting readme ([`be792ce`](https://github.com/evervault/evervault-python/commit/be792cebff11d3e6b6c23c58e86af34d1a8122be))

* define default args, update readme ([`07c9898`](https://github.com/evervault/evervault-python/commit/07c98985d1860e47c1925250d3eb23ba5bd544b6))

* add tests, fix version system ([`c63558a`](https://github.com/evervault/evervault-python/commit/c63558a4516517fb347b5fa9eb8f3456fd1a1539))

* update author details ([`725990e`](https://github.com/evervault/evervault-python/commit/725990eadaeb33877188af4f76ce89ec80f1fb55))

* add support, add documentation to readme ([`a738aeb`](https://github.com/evervault/evervault-python/commit/a738aebfe114e894c03a80c1abb366ad36b721b1))

* Merge pull request #10 from evervault/jonny/remove_evervault_client

Update readme to remove reference to evervault_client ([`c13a105`](https://github.com/evervault/evervault-python/commit/c13a105900b5cfa9946d69de643709f917d25669))

* Update readme to remove reference to evervault_client ([`f22014b`](https://github.com/evervault/evervault-python/commit/f22014b157e6627c0f5cfe0cea31d8288f5c515a))

* Add CODEOWNERS, PR templates ([`40a5b55`](https://github.com/evervault/evervault-python/commit/40a5b55c07496ad4102efe93ab52a80565434350))

* Add basic tests to evervault package (#9)

* Add basic tests to evervault package

* Use setup

* Use flake sure:

* Add requirements.txt

* Don&#39;t need 3.5 ([`7ed6c21`](https://github.com/evervault/evervault-python/commit/7ed6c211a69a4f5b31c8bbba43d8b4b1ddd10982))

* Merge pull request #8 from evervault/jonny/better-import

Import package instead of client ([`447951a`](https://github.com/evervault/evervault-python/commit/447951aa545f2db2e596e750532c70631fefd9a2))

* Include version file ([`5929024`](https://github.com/evervault/evervault-python/commit/5929024c5e60e6da21b486e48a9005a46e7f1d7f))

* Fix up client ([`36e3cd3`](https://github.com/evervault/evervault-python/commit/36e3cd3d1f559a2a87204b15c8994de0180a2117))

* Raise an error without an api key ([`b622f93`](https://github.com/evervault/evervault-python/commit/b622f9312edbf0f0b2fe7d12e7786e7609e81d1f))

* Import package instead of client ([`f0d0f77`](https://github.com/evervault/evervault-python/commit/f0d0f777ba446bd8dd2c27693edcf2a22c1a29e2))

* Change name ([`0bc87e6`](https://github.com/evervault/evervault-python/commit/0bc87e66b3a352af69956f2a0bf014737e512990))

* Version 0.0.1 for proper release ([`a4fcb5d`](https://github.com/evervault/evervault-python/commit/a4fcb5dd45c509df183625dd13b53ebaa9ef6ad5))

* Fix long_description, bump to v0.1.1 ([`922e368`](https://github.com/evervault/evervault-python/commit/922e368c7aa8a3c914e7a20a4cd0578a3d9b4c40))

* Update setup.py ([`9265190`](https://github.com/evervault/evervault-python/commit/92651901ebca2c56626f89e7817c1acb57942ca4))

* cage-run ([`25943a7`](https://github.com/evervault/evervault-python/commit/25943a79cb8e4af886f3231f5b8fa8abbfa2e736))

* Merge pull request #7 from evervault/jonny/cage-list

CageList object is neater ([`01c4d2e`](https://github.com/evervault/evervault-python/commit/01c4d2e33ca9e0f7d3ddafb53bcfa6f0730804a1))

* CageList object is neater ([`00f8db4`](https://github.com/evervault/evervault-python/commit/00f8db42293d42ab39497b26eb3ad251b7e18a38))

* Merge pull request #6 from evervault/jonny/readme

First draft readme ([`34fbea7`](https://github.com/evervault/evervault-python/commit/34fbea7ec2f57e94357b594f212c3f9ec0a8c37b))

* python not js ([`aa8cbf8`](https://github.com/evervault/evervault-python/commit/aa8cbf85f5af04fa79de7c7177b9718f0a46baf8))

* Capital e ([`42119d6`](https://github.com/evervault/evervault-python/commit/42119d64dabe7faaca995170b3b125cd294bc90d))

* First draft readme ([`fcc79a8`](https://github.com/evervault/evervault-python/commit/fcc79a84c870ecbd332d507e06c5a2f1bf838604))

* Merge pull request #5 from evervault/jonny/list-cages

Create cage objects that can be run as well ([`28c79b7`](https://github.com/evervault/evervault-python/commit/28c79b75eede75b5220d55d89b8768f27f50709c))

* Include cage models ([`9412caa`](https://github.com/evervault/evervault-python/commit/9412caa8fd2a09a876804737b1559248bbe9fdba))

* Create cage objects that can be run as well ([`6ca4208`](https://github.com/evervault/evervault-python/commit/6ca4208a881d21cb42628be8e2628a657aea617d))

* Merge pull request #4 from evervault/jonnyom/ch2461/run-cages

Run cages from python SDK and fix crypto client to only load cage key once per lifecycle of evervault client instance ([`0835d08`](https://github.com/evervault/evervault-python/commit/0835d08503c26a0f1d5a8625120a8c8a5fde1512))

* Run cages from python SDK and fix crypto client to only load cage key once per lifecycle of evervault client instance ([`df53382`](https://github.com/evervault/evervault-python/commit/df53382847eb78e340edafb0eed8b2ad8df032d2))

* Merge pull request #3 from evervault/jonnyom/ch2466/crypto-client-encrypt-objects

Encrypt nested objects ([`4a0b81e`](https://github.com/evervault/evervault-python/commit/4a0b81ed6526f8a3f9332fe2b9949a2c9823b8a2))

* Encrypt nested objects ([`351fb29`](https://github.com/evervault/evervault-python/commit/351fb296c29f29f88621f6e4e32ccc8f111a062b))

* Merge pull request #2 from evervault/jonnyom/ch2462/crypto-client/encrypt-strings

Encrypt strings with the Python SDK ([`5136629`](https://github.com/evervault/evervault-python/commit/51366299abc4482a986a9eaede55b017a8697436))

* Remove coding thing ([`2b21efe`](https://github.com/evervault/evervault-python/commit/2b21efe71d3f0158d899cb8e794e552c8f86de29))

* Include datatype mapper ([`07db671`](https://github.com/evervault/evervault-python/commit/07db671bba8373748fb46a6efaf0b3db0b8e2912))

* Encrypt strings with the Python SDK ([`eb09178`](https://github.com/evervault/evervault-python/commit/eb09178e13867e0e1577608256f87c8863619976))

* Merge pull request #1 from evervault/jonnyom/ch2462/crypto-client/first-pass-validating-input

Create crypto client - fetches cage key and sets it ([`0dfee32`](https://github.com/evervault/evervault-python/commit/0dfee32b6cecc99aa8afbb158bdee1b585153681))

* Include new files ([`feae102`](https://github.com/evervault/evervault-python/commit/feae102bfd4dd425cd3046b64aa975834a073f36))

* Create crypto client - fetches cage key and sets it ([`80377aa`](https://github.com/evervault/evervault-python/commit/80377aa8e2e5e922c9cdd619d0002fabc2691340))

* Correct python indenting ([`1ac03dc`](https://github.com/evervault/evervault-python/commit/1ac03dc7fea7ec0ca77f403acfa219e89ffe79f0))

* Bad tabs? ([`cdcbe8c`](https://github.com/evervault/evervault-python/commit/cdcbe8cb6c5576f6a544e824bdf756646b420754))

* Newline ([`bd772c4`](https://github.com/evervault/evervault-python/commit/bd772c467e32e1e03269c031f74e55358dc775ae))

* Unnecessary import ([`412e208`](https://github.com/evervault/evervault-python/commit/412e2080161e8db4d59ea9a9e3f4058612ffcce5))

* Cleaner request class ([`f9306f3`](https://github.com/evervault/evervault-python/commit/f9306f3c189ca7ff9ee54ffba2e9181973c34cbb))

* Initial commit - includes basic HTTP request class and HTTP client. ([`9a8f183`](https://github.com/evervault/evervault-python/commit/9a8f18381e306cd6edfece0ab77f2ce4f8640582))

// when compiling, batch_verfier becomes BatchVerifier, that's why we need to require BatchVerifier instead here.
const Batch_Verifier2 = artifacts.require("BatchVerifier2");
const BatchVerifier4_chainChallenge = artifacts.require("BatchVerifier4_chainChallenge");

module.exports = function (deployer) {
  deployer.deploy(Batch_Verifier2);
  deployer.deploy(BatchVerifier4_chainChallenge);
};
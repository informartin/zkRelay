// when compiling, batch_verfier becomes BatchVerifier, that's why we need to require BatchVerifier instead here.
const Batch_Verifier2 = artifacts.require("BatchVerifier2");

module.exports = function (deployer) {
  deployer.deploy(Batch_Verifier2);
};
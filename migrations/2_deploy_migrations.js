const CompanyStructCrud = artifacts.require("CompanyStructCrud");

module.exports = function (deployer) {
  deployer.deploy(CompanyStructCrud);
};

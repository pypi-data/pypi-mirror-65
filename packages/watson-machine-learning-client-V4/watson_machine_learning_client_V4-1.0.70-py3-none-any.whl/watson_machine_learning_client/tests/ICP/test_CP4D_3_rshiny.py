import unittest,time

from watson_machine_learning_client.log_util import get_logger
from watson_machine_learning_client.tests.ICP.preparation_and_cleaning import *
from watson_machine_learning_client.tests.ICP.models_preparation import *


class TestRshinyApp(unittest.TestCase):
    runtime_uid = None
    deployment_uid = None
    function_uid = None
    scoring_url = None
    logger = get_logger(__name__)

    @classmethod
    def setUpClass(self):
        TestRshinyApp.logger.info("Service Instance: setting up credentials")

        self.wml_credentials = get_wml_credentials()
        self.client = get_client()



        self.space = self.client.spaces.store({self.client.spaces.ConfigurationMetaNames.NAME: "test_case_Rshiny_app" + time.asctime() })
        TestRshinyApp.space_id = self.client.spaces.get_uid(self.space)
        self.client.set.default_space(TestRshinyApp.space_id)

    # def test_01_service_instance_details(self):
    #     TestAIFunction.logger.info("Check client ...")
    #     self.assertTrue(self.client.__class__.__name__ == 'WatsonMachineLearningAPIClient')
    #
    #     TestAIFunction.logger.info("Getting instance details ...")
    #     details = self.client.service_instance.get_details()
    #     TestAIFunction.logger.debug(details)
    #
    #     self.assertTrue("published_models" in str(details))
    #     self.assertEqual(type(details), dict)

    def test_01_create_shiny_asset(self):

        self.client.shiny.ConfigurationMetaNames.show()


        meta_prop_shiny = {
            self.client.shiny.ConfigurationMetaNames.NAME: "my shiny app",
            self.client.shiny.ConfigurationMetaNames.DESCRIPTION: "shiny app for deployment"
        }

        shiny_details = self.client.shiny.store(meta_prop_shiny, file_path="artifacts/app.R.zip")

        TestRshinyApp.shiny_asset_uid = self.client.shiny.get_uid(shiny_details)
        TestRshinyApp.shiny_asset_url = self.client.shiny.get_href(shiny_details)
        TestRshinyApp.logger.info("shiny asset ID:" + str(TestRshinyApp.shiny_asset_uid))
        TestRshinyApp.logger.info("shiny asset URL:" + str(TestRshinyApp.shiny_asset_url))
        self.assertIsNotNone(TestRshinyApp.shiny_asset_uid)
        self.assertIsNotNone(TestRshinyApp.shiny_asset_url)


    def test_02_download_shiny_content(self):
        try:
            os.remove('test_shiny_asset.zip')
        except:
            pass
        self.client.shiny.download(TestRshinyApp.shiny_asset_uid, filename='test_shiny_asset.zip')
        try:
            os.remove('test_shiny_asset.zip')
        except:
            pass

    def test_04_get_details(self):

        details = self.client.shiny.get_details(TestRshinyApp.shiny_asset_uid)
        self.assertTrue(TestRshinyApp.shiny_asset_uid in str(details))

    def test_05_list(self):
        self.client.shiny.list()

    def test_06_create_deployment(self):
        deploy_meta = {
                self.client.deployments.ConfigurationMetaNames.NAME: "deployment_rshiny",
                self.client.deployments.ConfigurationMetaNames.DESCRIPTION: "deployment rshiny deployment",
                self.client.deployments.ConfigurationMetaNames.R_SHINY: {"authentication" : "anyone_with_url" },
                self.client.deployments.ConfigurationMetaNames.HARDWARE_SPEC: {"name":"S", "num_nodes":1}
            }

        TestRshinyApp.logger.info("Create deployment")
        deployment = self.client.deployments.create(artifact_uid=TestRshinyApp.shiny_asset_uid, meta_props=deploy_meta)
        TestRshinyApp.logger.debug("deployment: " + str(deployment))
        # TestRshinyApp.scoring_url = self.client.deployments.get_scoring_href(deployment)
        # TestRshinyApp.logger.debug("Scoring href: {}".format(TestRshinyApp.scoring_url))
        TestRshinyApp.deployment_uid = self.client.deployments.get_uid(deployment)
        TestRshinyApp.logger.debug("Deployment uid: {}".format(TestRshinyApp.deployment_uid))
        self.client.deployments.list()
        self.assertTrue("deployment_rshiny" in str(deployment))

    def test_07_update_deployment(self):
        patch_meta = {
            self.client.deployments.ConfigurationMetaNames.DESCRIPTION: "deployment_Updated_Shiny_Description",
        }
        self.client.deployments.update(TestRshinyApp.deployment_uid, patch_meta)

    def test_08_get_deployment_details(self):
        TestRshinyApp.logger.info("Get deployment details")
        deployment_details = self.client.deployments.get_details()
        TestRshinyApp.logger.debug("Deployment details: {}".format(deployment_details))
        self.assertTrue('deployment_Updated_Shiny_Description' in str(deployment_details))

    def test_10_delete_deployment(self):
        TestRshinyApp.logger.info("Delete deployment")
        self.client.deployments.delete(TestRshinyApp.deployment_uid)

    def test_11_delete_shiny_asset(self):
        TestRshinyApp.logger.info("Delete function")
        self.client.shiny.delete(TestRshinyApp.shiny_asset_uid)
        self.client.spaces.delete(TestRshinyApp.space_id)


if __name__ == '__main__':
    unittest.main()

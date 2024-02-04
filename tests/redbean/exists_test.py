from redbeanpython import Bean
from tests.redbean.abstract import RedBeanTestAbstract


class TestRedBeanExists(RedBeanTestAbstract):
    def test_exists(self):
        namespace = f"test_via_env_dir{self.test_hash()}"
        directory = f"/tmp/{namespace}"

        rb = self.get_red_bean(directory=directory, namespace=namespace)
        bean_id = rb.store(Bean(self.BEAN_TYPE, {"any": "any"}))

        assert rb.exists(self.BEAN_TYPE, bean_id=bean_id)
        assert not rb.exists(self.BEAN_TYPE, bean_id="other_bean_id")
        assert not rb.exists("not_existing_bean_type", bean_id=bean_id)

        rb = self.get_red_bean(directory=directory, namespace=namespace, frozen=True)

        assert rb.exists(self.BEAN_TYPE, bean_id=bean_id)
        assert not rb.exists(self.BEAN_TYPE, bean_id="other_bean_id")
        assert not rb.exists("not_existing_bean_type", bean_id=bean_id)

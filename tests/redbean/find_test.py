from redbeanpython import Bean
from tests.redbean.abstract import RedBeanTestAbstract


class TestRedBeanFind(RedBeanTestAbstract):
    def test_base_path_of_storing_extending_and_fetching_results(self):
        rb = self.get_red_bean()
        test_data = [
            {"id": "1", "x": 10, "y": True},
            {"id": "2", "x": 20, "y": True},
            {"id": "3", "x": 30, "y": False},
            {"id": "4", "x": 40, "y": False},
        ]
        assert list(rb.find(self.BEAN_TYPE)) == []
        for data in test_data:
            rb.store(Bean(self.BEAN_TYPE, data))

        assert list(rb.find(self.BEAN_TYPE)) == [
            Bean(self.BEAN_TYPE, test_data[0]),
            Bean(self.BEAN_TYPE, test_data[1]),
            Bean(self.BEAN_TYPE, test_data[2]),
            Bean(self.BEAN_TYPE, test_data[3]),
        ]

        assert list(rb.find(self.BEAN_TYPE, query="x > :x_v", params={"x_v": 10})) == [
            Bean(self.BEAN_TYPE, test_data[1]),
            Bean(self.BEAN_TYPE, test_data[2]),
            Bean(self.BEAN_TYPE, test_data[3]),
        ]

        assert list(
            rb.find(self.BEAN_TYPE, query="x > :x_v", params={"x_v": 10}, limit=2)
        ) == [
            Bean(self.BEAN_TYPE, test_data[1]),
            Bean(self.BEAN_TYPE, test_data[2]),
        ]

        assert list(
            rb.find(
                self.BEAN_TYPE, query="x > :x_v", params={"x_v": 10}, limit=2, offset=1
            )
        ) == [
            Bean(self.BEAN_TYPE, test_data[2]),
            Bean(self.BEAN_TYPE, test_data[3]),
        ]

        assert list(
            rb.find(
                self.BEAN_TYPE,
                query="x > :x_v",
                params={"x_v": 10},
                limit=2,
                order="id DESC",
            )
        ) == [
            Bean(self.BEAN_TYPE, test_data[3]),
            Bean(self.BEAN_TYPE, test_data[2]),
        ]

        assert list(rb.find("not_existing_bean_type")) == []

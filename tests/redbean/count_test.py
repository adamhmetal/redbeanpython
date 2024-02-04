from tests.redbean.abstract import RedBeanTestAbstract


class TestRedBeanCount(RedBeanTestAbstract):
    def test_count(self):
        rb = self.get_red_bean()
        assert rb.count(self.BEAN_TYPE) == 0
        rb.store(rb.dispense(self.BEAN_TYPE, data={"x": 10, "y": True}))
        rb.store(rb.dispense(self.BEAN_TYPE, data={"x": 20, "y": True}))
        rb.store(rb.dispense(self.BEAN_TYPE, data={"x": 30, "y": False}))
        rb.store(rb.dispense(self.BEAN_TYPE, data={"x": 40, "y": False}))

        assert rb.count(self.BEAN_TYPE) == 4

        assert rb.count(self.BEAN_TYPE, query="x > :x_val", params={"x_val": 10}) == 3
        assert (
            rb.count(
                self.BEAN_TYPE,
                query="(x > :x_v) and (y = :y_v) ",
                params={"x_v": 10, "y_v": False},
            )
            == 2
        )

        assert rb.count("not_existing_bean_type") == 0

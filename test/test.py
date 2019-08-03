from src.pub import Publisher


def test_publisher():
    pub = Publisher()
    data = {'title': 'test'}
    pub.do_publish(data)


if __name__ == '__main__':
    test_publisher()

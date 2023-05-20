from associative_processor import Processor

if __name__ == '__main__':
    associative_processor = Processor(3, 10)
    print(associative_processor)
    print(associative_processor.find_the_closest_value([1, 0, 1], below=True))
    print(associative_processor.get_sort_list(reverse=True))


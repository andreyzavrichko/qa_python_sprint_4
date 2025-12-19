import pytest

class TestBooksCollector:

    def test_add_new_book_add_two_books(self, collector):
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        assert len(collector.get_books_genre()) == 2

    @pytest.mark.parametrize('book_name', [
        '',
        'a' * 41,
        'a' * 255,
    ])
    def test_add_new_book_invalid_name_not_added(self, collector, book_name):
        collector.add_new_book(book_name)
        assert book_name not in collector.get_books_genre()

    def test_add_new_book_duplicate_not_added(self, collector):
        collector.add_new_book('Гарри Поттер и философский Парень')
        collector.add_new_book('Гарри Поттер и философский Парень')
        assert list(collector.get_books_genre().keys()).count('Гарри Поттер и философский Парень') == 1

    def test_add_new_book_added_without_genre(self, collector):
        collector.add_new_book('Гарри Поттер')
        assert collector.get_book_genre('Гарри Поттер') == ''

    @pytest.mark.parametrize('genre', ['Детективы', 'Комедии', 'Фантастика'])
    def test_set_book_genre_valid_genre_sets_correctly(self, collector, genre):
        collector.add_new_book('Гарри Поттер')
        collector.set_book_genre('Гарри Поттер', genre)
        assert collector.get_book_genre('Гарри Поттер') == genre

    def test_set_book_genre_invalid_genre_not_set(self, collector):
        collector.add_new_book('Гарри Поттер')
        collector.set_book_genre('Гарри Поттер', 'Несуществующий жанр')
        assert collector.get_book_genre('Гарри Поттер') == ''

    def test_set_book_genre_nonexistent_book_not_set(self, collector):
        collector.set_book_genre('Несуществующая книга', 'Фантастика')
        assert 'Несуществующая книга' not in collector.get_books_genre()

    def test_add_book_in_favorites_adds_existing_book(self, collector):
        collector.add_new_book('Гарри Поттер')
        collector.add_book_in_favorites('Гарри Поттер')
        assert 'Гарри Поттер' in collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_nonexistent_book_not_added(self, collector):
        collector.add_book_in_favorites('Несуществующая книга')
        assert collector.get_list_of_favorites_books() == []

    def test_add_book_in_favorites_duplicate_not_added(self, collector):
        collector.add_new_book('Гарри Поттер')
        collector.add_book_in_favorites('Гарри Поттер')
        collector.add_book_in_favorites('Гарри Поттер')
        assert collector.get_list_of_favorites_books().count('Гарри Поттер') == 1

    def test_delete_book_from_favorites_removes_book(self, collector):
        collector.add_new_book('Гарри Поттер')
        collector.add_book_in_favorites('Гарри Поттер')
        collector.delete_book_from_favorites('Гарри Поттер')
        assert 'Гарри Поттер' not in collector.get_list_of_favorites_books()

    def test_get_books_for_children_excludes_age_rated_genres(self, collector):
        collector.add_new_book('Рапунцель')
        collector.add_new_book('Форсаж 19')
        collector.add_new_book('Один дома')
        collector.add_new_book('Оно')

        collector.set_book_genre('Рапунцель', 'Мультфильмы')
        collector.set_book_genre('Форсаж 19', 'Фантастика')
        collector.set_book_genre('Один дома', 'Комедии')
        collector.set_book_genre('Оно', 'Ужасы')

        children_books = collector.get_books_for_children()
        assert 'Рапунцель' in children_books
        assert 'Форсаж 19' in children_books
        assert 'Один дома' in children_books
        assert 'Оно' not in children_books

    @pytest.mark.parametrize('genre, expected_books', [
        ('Фантастика', ['Марсианин', 'Грань будущего']),
        ('Ужасы', ['Оно']),
        ('Комедии', []),
    ])
    def test_get_books_with_specific_genre_returns_correct_list(self, collector, genre, expected_books):
        collector.add_new_book('Марсианин')
        collector.add_new_book('Грань будущего')
        collector.add_new_book('Оно')
        collector.set_book_genre('Марсианин', 'Фантастика')
        collector.set_book_genre('Грань будущего', 'Фантастика')
        collector.set_book_genre('Оно', 'Ужасы')

        assert sorted(collector.get_books_with_specific_genre(genre)) == sorted(expected_books)
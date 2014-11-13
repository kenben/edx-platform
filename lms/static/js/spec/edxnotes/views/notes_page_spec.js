define(['jquery', 'underscore', 'js/edxnotes/views/notes_page', 'js/edxnotes/collections/notes', 'jasmine-jquery'],
    function($, _, NotesPage, NotesCollection) {
        'use strict';

        describe('NotesPage', function() {
            var view;

            var initializePage = function () {
                var collection;

                collection = new NotesCollection([
                    {
                        updated: Date.UTC(2014,10,10,10,10,10,12),
                        text: 'Third listed'
                    },
                    {
                        updated: Date.UTC(2014,10,10,10,10,10,10),
                        text: 'First listed'
                    },
                    {
                        updated: Date.UTC(2014,10,10,10,10,10,11),
                        text: 'Second listed'
                    }
                ]);

                return new NotesPage({collection: collection});
            };

            beforeEach(function() {
                view = initializePage();
                view.render();
            });

            describe('Basic', function() {
                it('should order notes in ascending UTC date', function() {
                    var highlights = view.$('article.edxnotes-page-item>div.note-quote');
                    expect(highlights.get(0).text()).toBe('First listed');
                    expect(highlights.get(1).text()).toBe('Second listed');
                    expect(highlights.get(2).text()).toBe('Third listed');
                });
            });
        });
    }
);

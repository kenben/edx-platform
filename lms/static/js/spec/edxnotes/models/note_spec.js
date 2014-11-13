define(['jquery', 'js/edxnotes/models/note', 'js/edxnotes/collections/notes', 'jasmine-jquery'],
    function($, NoteModel, NotesCollection) {
        'use strict';

        describe('NoteModel', function() {
            var model;

            beforeEach(function() {
                model = new NoteModel();
            });

            describe('Basic', function() {
                it('should have a null id by default', function() {
                    expect(model.get('id')).toBeNull();
                });
                // TODO...
            });
        });

        describe('NotesCollection', function() {
            var collection;

            beforeEach(function() {
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
            });

            describe('Basic', function() {
                it('should order notes in ascending UTC date', function() {
                    expect(collection.at(0).get('text')).toBe('First listed');
                    expect(collection.at(1).get('text')).toBe('Second listed');
                    expect(collection.at(2).get('text')).toBe('Third listed');
                });
            });
            // TODO...
        });
    }
);

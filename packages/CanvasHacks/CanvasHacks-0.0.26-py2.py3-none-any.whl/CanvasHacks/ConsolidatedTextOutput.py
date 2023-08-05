"""
This contains tools for displaying all student submitted
text along with toggle buttons for assigning credit or
no credit

For testing

# credit_list = [0, 2]

# make_consolidated_text_fields(test_results, credit_list)

Created by adam on 2/5/19
"""
__author__ = 'adam'
import json

from IPython.display import display
from ipywidgets import widgets


def make_assignment_header( store ):
    """Displays the header for each unit"""
    entry = """
    <h1>{}</h1>
    <h2>Class id: {}</h2>"""
    return display( widgets.HTML( entry.format( store.assignment_name, store.course_id ) ) )


def make_text_display( student_id, text ):
    """Handles the formatting of the student's text"""
    entry = """
          <div id='%s'>
            <h3>%s</h3>
            <p>
                %s
            </p>
        </div>"""
    e = entry % (student_id, student_id, text)
    return widgets.HTML( e )


def make_submission_output( text, student_id, credit_list ):
    """Creates the display of the submitted text with a toggle button to
    update whether the student receives credit
    """
    bval = 'Credit' if student_id in credit_list else 'No credit'
    credit_button = widgets.ToggleButtons(
        options=[ 'Credit', 'No credit' ],
        value=bval,
        description='',
        disabled=False
    )

    ta = make_text_display( student_id, text )

    def on_value_change( change ):
        """The relevant callback
        NB the use of scope to define student_id"""
        v = change[ 'new' ]
        print( v, student_id )
        try:
            if v == 'Credit':
                credit_list.append( student_id )
            elif v == 'No credit':
                credit_list.remove( student_id )
        except ValueError:
            pass

    credit_button.observe( on_value_change, names='value' )
    display( widgets.VBox( [ ta, credit_button ] ) )


def make_consolidated_text_fields( store ):
    """Displays each entry with a toggle to adjust whether the
    student receives credit"""
    for r in store.submissions:
        make_submission_output( r[ 'body' ], r[ 'student_id' ], store.credit )


def make_consolidated_text_file( journal_folder, filename='compiled-text.txt' ):
    """Reads the data from the relevant json file and then
    writes each entry in to a single text file for ease of reading
    """
    entry = """
    {student_id} \n
    {body} \n
    \n
    """
    to_write = "%s/%s" % (journal_folder, filename)
    with open( "%s/all-submissions.json" % journal_folder, 'r' ) as f:
        j = json.load( f )
        with open( to_write, 'w+' ) as cf:
            for rec in j:
                #     print(entry.format(**rec))
                cf.write( entry.format( **rec ) )
    print( "Consolidated file written to {}".format( to_write ) )


def make_test_data( number_students ):
    return [ { 'student_id': i, 'body': 'Body text for student {}'.format( i ) } for i in range( 0, number_students ) ]


if __name__ == '__main__':
    pass

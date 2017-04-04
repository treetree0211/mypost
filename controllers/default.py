# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index1():
    """
    lets users login or logout
    """
    # for development purposes only:
    print auth.user_id

    return dict()


def index():
    """
    lets users login or logout
    """
    original_rows = db(db.post.user_id>0).select(limitby = (0,10))
    rows = []
    row_length = len(original_rows)
    for row in original_rows :
        rows.append(original_rows[row_length - 1])
        row_length = row_length - 1

    return dict(rows=rows)

@auth.requires_login()
def votes_up():
    item = db.post[request.vars.id]
    new_votes_up = item.votes_up + 1
    item.update_record(votes_up=new_votes_up)

    return str(new_votes_up)

@auth.requires_login()
def votes_down():
    item = db.post[request.vars.id]
    new_votes_down = item.votes_down + 1
    item.update_record(votes_down=new_votes_down)

    return str(new_votes_down)

@auth.requires_login()
def edit():
    post = db.post[request.args(0)]
    if not post:
        form = SQLFORM(db.post,
                labels= {'post_subject': "Subject", 'post_content': "Content"},
                submit_button = 'Submit your post',
                )

        if form.process(keepvalues=True).accepted:
            response.flash = 'post accepted'

        elif form.errors:
            response.flash = 'please complete your post'
        else:
            response.flash = 'please post your content'

        return dict(form=form)
    elif post.user_id != auth.user_id:
        redirect(URL('index'))

    form = SQLFORM(db.post, post,
                 labels= {'post_subject': "Subject", 'post_content': "Content"},
                 showid= False,
                 deletable= True,
                 submit_button = 'Update your edit',
                  )

    if form.process(keepvalues=True).accepted:
       response.flash = 'edit accepted'

    elif form.errors:
       response.flash = 'please complete your post'
    else:
       response.flash = 'please edit your content'

    return dict(form=form)


@auth.requires_login()
def create_post():
    """form for posting a  new comment"""
    form = SQLFORM(db.post,
            labels= {'post_subject': "Subject", 'post_content': "Content"},
            submit_button = 'Submit your post',
            )

    if form.process(keepvalues=True).accepted:
       response.flash = 'post accepted'

    elif form.errors:
       response.flash = 'please complete your post'
    else:
       response.flash = 'please post your content'

    return dict(form=form)


@auth.requires_login()
def edit_post():
    """form for editing an existing post"""
    post = db.post[request.args(0)]
    if not(post and post.user_id == auth.user_id):
        redirect(URL('index'))
    form = SQLFORM(db.post, post,
                 labels= {'post_subject': "Subject", 'post_content': "Content"},
                 showid= False,
                 deletable= True,
                 submit_button = 'Update your edit',
                  )

    if form.process(keepvalues=True).accepted:
       response.flash = 'edit accepted'

    elif form.errors:
       response.flash = 'please complete your post'
    else:
       response.flash = 'please edit your content'

    return dict(form=form)


@auth.requires_login()
def delete():
    p = db.post(request.args(0)) or redirect(URL('default', 'index'))
    if p.user_id != auth.user_id:
        session.flash = 'form not authorized'
        redirect(URL('default', 'index'))
    db(db.post.id == p.id).delete()
    redirect(URL('default', 'index'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)



# Field Notes — a basic Django blog

A small, fully functional Django blog built for the Week 1 task. Visitors can
browse posts, read individual entries, and leave comments. Logged-in users
(post authors) can publish new entries through a web form.

## Project structure

```
django_blog/
├── manage.py                  # Django's command-line entry point
├── requirements.txt           # Python dependencies (Django)
├── README.md                  # This file
├── .gitignore
├── blogproject/                # Project-level configuration
│   ├── __init__.py
│   ├── settings.py             # App registration, database, templates, static files
│   ├── urls.py                 # Root URL conf — delegates to blog.urls
│   ├── wsgi.py
│   └── asgi.py
└── blog/                       # The blog app itself
    ├── __init__.py
    ├── apps.py
    ├── admin.py                 # Registers Post/Comment in Django admin
    ├── models.py                # Post and Comment models
    ├── forms.py                 # PostForm and CommentForm (ModelForms)
    ├── views.py                 # post_list, post_detail, post_create
    ├── urls.py                  # App-level URL patterns, namespaced "blog"
    ├── migrations/
    │   ├── __init__.py
    │   └── 0001_initial.py      # Initial schema for Post and Comment
    ├── templates/blog/
    │   ├── base.html            # Shared layout: header, nav, messages, footer
    │   ├── post_list.html       # Paginated list of all posts
    │   ├── post_detail.html     # Single post + comments + comment form
    │   └── post_form.html       # "New entry" form (author only)
    └── static/blog/css/
        └── style.css            # All styling (responsive, no framework)
```

## Data model

**Post**
- `title` — CharField
- `slug` — SlugField, auto-generated from the title and guaranteed unique
  (used to build clean URLs like `/post/my-first-entry/`)
- `content` — TextField
- `author` — ForeignKey to Django's built-in `User`
- `published_date` — set automatically on creation
- `updated_date` — set automatically on every save

**Comment**
- `post` — ForeignKey to `Post` (`related_name="comments"`)
- `author_name` — plain text field (no account required to comment)
- `content` — TextField
- `created_date` — set automatically on creation

This keeps commenting frictionless (no signup required) while posting stays
gated behind authentication, which is a common pattern for small blogs: one
or a few trusted authors, an open comment section.

## Views & routing

| URL                     | View          | Purpose                                      |
|--------------------------|--------------|-----------------------------------------------|
| `/`                      | `post_list`   | Paginated (5/page) list of all posts, newest first |
| `/post/<slug>/`          | `post_detail` | Shows one post, its comments, and a comment form (handles the POST too) |
| `/post/new/`             | `post_create` | Form to publish a new post — requires login (`@login_required`) |
| `/admin/`                | Django admin  | Manage posts, comments, and users             |

`post_detail` and `post_create` both use Django's `ModelForm` (`CommentForm`,
`PostForm`) for validation and rendering, and both redirect (POST/redirect/GET
pattern) after a successful submission to avoid duplicate form resubmission
on refresh. `get_object_or_404` is used for the detail view so a missing slug
returns a proper 404 instead of a server error.

## How to run it

1. **Create a virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate        # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Apply migrations** (creates `db.sqlite3` with the Post/Comment tables)
   ```bash
   python manage.py migrate
   ```

3. **Create a superuser** so you can log in and publish posts
   ```bash
   python manage.py createsuperuser
   ```

4. **Run the development server**
   ```bash
   python manage.py runserver
   ```

5. Visit `http://127.0.0.1:8000/` to browse the blog, or
   `http://127.0.0.1:8000/admin/` to log in and manage content. Once logged
   in, the "New entry" link appears in the site navigation and takes you to
   `http://127.0.0.1:8000/post/new/`.

> Note: this project uses Django's built-in admin login (`/admin/login/`) as
> the sign-in page for post authors, rather than building a separate login
> view, since Week 1's scope is focused on posts/comments/routing rather than
> a custom auth system.

## Design decisions & notes

- **Slugs over numeric IDs in URLs.** `Post.save()` auto-generates a unique
  slug from the title so URLs are readable (`/post/my-first-entry/`) instead
  of `/post/1/`. Collisions are handled by appending an incrementing suffix.
- **Comments don't require an account.** `author_name` is a free-text field
  rather than a ForeignKey to `User`, so any reader can comment without
  registering — a deliberate tradeoff for a simple blog. Posting a new
  *entry*, however, does require authentication, since that's the action
  worth protecting.
- **Pagination** is handled with Django's built-in `Paginator` (5 posts per
  page) so the list view stays fast and usable as the blog grows.
- **No JavaScript framework** — templates are server-rendered Django
  templates with one hand-written, responsive stylesheet (`style.css`), kept
  dependency-free and easy to read.
- **Styling** follows an editorial "field notes / journal" theme: a warm
  sage/paper background with a faint ruled-notebook texture, a serif display
  face for headings, numbered entry markers on the list page, and dashed
  dividers between posts and comments. It's fully responsive down to mobile
  widths, with visible keyboard focus states.

## Challenges encountered

- **Unique, human-readable URLs.** Deriving slugs from titles meant handling
  the case where two posts share a title; the `Post.save()` override loops
  and appends a numeric suffix (`-2`, `-3`, ...) until it finds a free slug.
- **Keeping the comment form frictionless without weakening the post-creation
  gate.** Splitting `CommentForm` (open) from `PostForm` (behind
  `@login_required`) kept both flows simple without over-engineering a
  permissions system for a Week 1 scope.
- **Avoiding duplicate submissions.** Both POST-handling views follow the
  Post/Redirect/Get pattern, redirecting to the detail view after a
  successful save rather than re-rendering the same page, so refreshing the
  result page doesn't resubmit the form.

## Possible next steps (out of scope for Week 1)

- Post editing/deletion views, and comment moderation
- A dedicated signup/login flow instead of relying on the admin login page
- Tags/categories and search
- Rich text or Markdown support for post content

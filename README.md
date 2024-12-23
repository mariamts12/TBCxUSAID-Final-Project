# Magic Loop Platform

## Overview
Magic Loop is a web-based platform designed for crochet and knitting enthusiasts. The platform allows users to manage patterns, projects, and community interactions effectively. Below are the core features divided by apps:

---

## 1. User App Features
- **JWT Authentication**
  - Users are authenticated using JSON Web Tokens (JWT).
- **Signup with Email and Username**
  - Users can register using their email and username.
- **Login with Username and Password**
  - Secure login functionality.
- **Email Confirmation**
  - After successful registration, an email is sent to the user.
  - **Celery** is used to handle periodic tasks for email delivery.

---

## 2. Community App
- **Post Creation**
  - Logged-in users can create posts, including images (to ask questions or share tips).
- **Interactions with Posts**
  - Users can like or unlike posts.
  - Users can comment on posts.
  - Users can pin comments on their own posts.
  - Users can like or dislike comments by others.
- **Filtering and Searching**
  - Posts can be filtered by tags.
  - Users can search posts by keywords in the title or content.
  - Users can view their own posts.
- **Pagination**
  - Pagination is implemented for post listings.
- **Post Deletion**
  - Users can delete their own posts.

---

## 3. Patterns App
- **Posting and Viewing Patterns**
  - Authenticated users can post patterns or view patterns posted by others.
- **Tags and Categories**
  - Patterns are organized with tags and categories.
  - Users can add their own tags.
- **Yarn Types**
  - Patterns specify recommended yarn types.
- **Materials Management**
  - Users can add materials to a pattern by specifying the material name, amount, and unit.
- **Saving Patterns**
  - Users can save or unsave patterns.
  - Users can view their saved patterns and their own patterns.
- **Guest Access**
  - Unauthenticated users can view the 15 most popular patterns (general info only).
  - Popular patterns are cached.
  - Popularity is determined by the number of users who saved the pattern.
- **Notifications**
  - When a pattern reaches a milestone number of saves, the author is notified via email.
  - **Celery** is used for this notification system.
- **Filtering and Searching**
  - Patterns can be filtered by tags, categories, yarn types, and difficulty.
  - Users can search patterns by title or description.
  - Patterns can also be filtered by user ID.
  - Patterns can be ordered by popularity.
- **Pagination**
  - Pagination is implemented for pattern listings.
- **Pattern Uploads**
  - Users can upload patterns as files or enter them in a text field.
- **Pattern Deletion**
  - Users can delete their own patterns.

---

## 4. Projects App
- **Project Management**
  - Users can create, update, and delete projects.
  - Projects can be associated with patterns (optional).
- **Specifications**
  - Users can specify yarn types, crochet hook sizes, or knitting needle sizes.
  - Users can add multiple photos to their projects.
- **Project Details**
  - Projects include a status (in progress or completed), start date, end date, and time spent.
  - The default status is "in progress."
  - The end date is automatically set to the day the status changes to "completed" or can be manually specified by the user.
- **Project Updates**
  - Users can update their projects with descriptions, tips, and experiences as the project progresses.
- **Viewing Projects**
  - Users can view their own projects and those of others.
- **Filtering and Searching**
  - Projects can be filtered by pattern ID, user ID, yarn type, status, and time spent.
  - Users can search for projects by name or description.

---

## Technologies and Features
- **Authentication**: JWT for secure user authentication.
- **Task Management**: Celery for handling asynchronous tasks, using Redis as the message broker.
- **Caching**: Popular patterns endpoint is cached for better performance.
- **Search and Filters**: Advanced search and filtering capabilities across all apps.
- **Pagination**: Implemented across posts, patterns, and projects.
- **Admin Panel**: The admin panel has been upgraded for better usability and management across all apps.

---

## Dependencies

- **Django**: Framework for building the web application.
- **Django REST Framework (DRF)**: For API development.
- **djangorestframework-simplejwt**: For JWT-based authentication.
- **drf-yasg**: For Swagger API documentation generation.
- **Celery**: For asynchronous task handling.
- **Redis**: Used as the message broker for Celery.
- **python-decouple**: For environment variable management.
- **django-filter**: For query parameter filtering.
- **django-debug-toolbar**: For debugging during development.

---

## Code Quality

To maintain high code quality, the following tools were used:

- **Black**: Ensures consistent code formatting.
- **Flake8**: Validates compliance with PEP 8 standards and helps catch common errors.

---

## Planned Features

Future plans for the project include adding:

- feedback to projects
- paid patterns
- store app for selling yarns, patterns, other materials/accessories
- OpenAI API for visual inspiration
- user rating system
- functionality to kind of randomly chose next pattern for user, according to users preferences and skills/rating
- enhancing localization support by adding more languages.

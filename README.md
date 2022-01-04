# Dicentra Backend
<div align="center"><img src="https://github.com/TyrelN/dicentra-frontend/blob/main/src/assets/nvars-logo-light.svg" width="300"/></div><br>

## About
Dicentra is a full-stack website designed for Nicola Valley Animal Rescue. The website acts as a platform for applications (to adopt, foster or volunteer), animal education, donations and more.

Visit the website here [here](https://www.nvars.ca/).
## Features

The backend of Dicentra maintains several important features:

### Pet Posts:
A tab for setting to-do list items and reminders. To-do list items are just that, and for more time-sensitive cases, you can set your to-do item as a reminder, which allows you to attach a date to it and schedule a notification for the date and time selected.


### Articles
This tab is for jotting down notes and thoughts you would like to keep and be able to find later. You can filter your notes by keywords and phrases to more efficiently find them over time.

### Applications
A gallery of images queried from the [picsum](https://picsum.photos/) api that can be selected to load a larger version of an image that can be scaled via two-touch pinching and one-touch panned. The current iteration is an expanded-upon version of the photo gallery exercise from [React Native Express](https://www.reactnative.express/exercises/photo_gallery).

### Help Wanted

### Current Events

## Design logic and process
There were numerous technical challenges involved with the design of the project. Some notable decisions made were as follows:
* To reduce repetition with large forms, the contact information was included as an abstract base class, that each specific form extends with their own personal questions.
* Since Django cannot store user submitted media (images) properly in production, [Cloudinary](https://cloudinary.com/) was implemented as a third-party cloud storage, which also allows for additional image optimization on image delivery via urls.
* Slugs were implemented in place of primary keys for detail pages and data identification to improve url readability. To decrease the chance of slug naming conflicts, a random token was attached to the end of each generated slug. 
* To remove the need for seperate update and create functionality on the frontend, the current event table only allows for a single entry that is updated if one exists and created if one doesn't.


## Areas in need of improvement
There are some areas of the design that should be noted and considered with regards ot the design:
* Automated Test Suite: A mixture of unit and integration tests are in the works to help the security and stability of the backend and ensure smoother updates in the future.
* Article image limit: Due to cpu limitations with affordable hosting platforms, the Article table should only upload up to three images per article post or patch.
* Article simplicity: While other articles and blog posts may use a more elaborate content management system, such a system was not within scope for this project. A more simple approach of a simple Articles model with limited fields was deemed appropriate for animal rescues.




## Additional Notes:
* The project is deployed on [Railway](https://railway.app/) using the Dockerfile in the root of the repo


## References and Resources
* https://steelkiwi.com/blog/practical-application-singleton-design-pattern/
* https://www.youtube.com/watch?v=Yg5zkd9nm6w
* https://www.django-rest-framework.org/
* https://docs.djangoproject.com/en/4.0/
* https://martinheinz.dev/blog/48
* https://realpython.com/modeling-polymorphism-django-python/?utm_source=pocket_mylist


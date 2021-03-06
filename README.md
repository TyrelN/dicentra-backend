# Dicentra (Backend)
<div align="center"><img src="https://github.com/TyrelN/dicentra-frontend/blob/main/src/assets/nvars-logo-light.svg" width="300"/></div>

## About
Dicentra is a full-stack website designed for Nicola Valley Animal Rescue. The website acts as a platform for applications (to adopt, foster or volunteer), animal education, donations and more.

Visit the website here [here](https://www.nvars.ca/).

View a showcase of the content management features [here](https://www.youtube.com/watch?v=vcnvZttQCXQ).
## Features

The backend of Dicentra maintains several important features:

### Pet Posts:
The animal residents of NVARS have their profiles stored on the backend, which can later be displayed to visitors and kept on file for volunteers as well.

### Articles:
Informative posts about animal care or events can be kept in the articles section, storing images, captions, links and more for a given article piece.

### Applications:
Visitors that submit applications have their information stored as either a foster, adopt or volunteer model that inherits from the abstract applicant class. Specific applications are then retrievable via slug identifiers to view on the frontend by volunteers.

### Help Wanted:
A section for volunteers to post desired volunteer positions and the duties they would include. Visitors to the website can then browse this page and apply with a volunteer position in mind.

### Current Events:
A section for posting news-worthy or seasonal events that volunteers would like visitors to see on the front page. A text field and an image are saved on the backend and new posts replace the same entry instead of creating new data columns.

### ER Diagram (Generated by Django-Extensions and Graphviz)
![er_diagram](https://user-images.githubusercontent.com/43082470/148185405-a4a0608b-4f74-41e6-aa78-031b86ed6a32.png)

Admin access is driven by the [djoser library](https://djoser.readthedocs.io/en/latest/getting_started.html) and allows for volunteers to submit updates to posts, delete posts and create new ones from the frontend.

## Design Choices
There were numerous technical challenges involved with the design of the project. Some notable decisions made were as follows:
* To reduce repetition with large forms, the contact information was included as an abstract base class, that each specific form extends with their own personal questions.
* Since Django cannot store user submitted media (images) properly in production, [Cloudinary](https://cloudinary.com/) was implemented as a third-party cloud storage, which also allows for additional image optimization on image delivery via urls.
* Slugs were implemented in place of primary keys for detail pages and data identification to improve url readability. To decrease the chance of slug naming conflicts, a random token was attached to the end of each generated slug. 
* To remove the need for seperate update and create functionality on the frontend, the current event table only allows for a single entry that is updated if one exists and created if one doesn't.


## Caveats
There are some areas of the design that should be addressed:
* Automated Test Suite: integration tests are in the works to help the security and stability of the backend, as well as enabling continuous integration.
* Article image limit: Due to cpu limitations with affordable hosting platforms, the Article table should only upload up to three images per article post or patch.
* Article simplicity: While other articles and blog posts may use a more elaborate content management system, such a system was not within scope for this project. An approach of an Articles model with limited fields was considered plenty, and the strict limits would not impede the animal rescue.


## Additional Notes:
* The api is deployed on [Heroku](https://www.heroku.com/what). The project has been deployed using both docker container registry and github integration, and is currently deployed with the latter.
* The backend api was developed using Docker, with a postgres database attached to the backend in a multi-container setup using Docker-Compose


## References and Resources
* https://steelkiwi.com/blog/practical-application-singleton-design-pattern/
* https://www.youtube.com/watch?v=Yg5zkd9nm6w
* https://www.django-rest-framework.org/
* https://docs.djangoproject.com/en/4.0/
* https://martinheinz.dev/blog/48
* https://realpython.com/modeling-polymorphism-django-python/?utm_source=pocket_mylist


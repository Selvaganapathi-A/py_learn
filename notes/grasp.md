# GRASP Design Patterns

**GRASP (General Responsibility Assignment Software Patterns)** is a set of principles that guide the assignment of responsibilities in object-oriented design.

These principles help in achieving a more maintainable and flexible design by ensuring proper allocation of responsibilities to classes and objects.

Here's an explanation of each **_GRASP principle_** with examples:

1. **Creator**:

    - The Creator principle states that a class should be responsible for creating instances of other classes if it has a composition or aggregation relationship with them.

    - This means that a class should create objects of other classes it contains or depends on.

    ___
    - For example, a `Customer` class may be responsible for creating instances of the `Order` class since it has a composition relationship with orders.
    ___

1. **Information Expert**:

    - The Information Expert principle suggests that a class should be assigned a responsibility if it has the necessary information to fulfill that responsibility.

    - The class that has the most relevant information to perform a specific task should be responsible for that task.

    ___
    - For example, a `BankAccount` class may be responsible for calculating _interest_ on the account since it holds the necessary information such as the _account balance_ and _interest rate_.
    ___

1. **High Cohesion**:

    - High Cohesion states that a class should have a single, well-defined responsibility and should be focused on fulfilling that responsibility.

    - This principle aims to keep classes focused and modular.

    ___
    - For example, a `FileParser` class should be responsible for parsing and extracting data from files, without having additional responsibilities like data validation or persistence.
    ___

1. **Low Coupling**:

    - Low Coupling suggests that classes should have minimal dependencies on each other.

    - It promotes loose coupling between classes, which increases the flexibility and maintainability of the system.

    - Each class should depend on abstractions rather than concrete implementations.

    ___
    - For example, a `PaymentProcessor` class should depend on an interface `PaymentGateway`, allowing different payment gateway implementations to be easily swapped without affecting the `PaymentProcessor` class.
    ___

1. **Controller**:

    - The Controller principle states that a class should be responsible for controlling the flow and coordination of actions within a system.

    - It acts as an intermediary between user interfaces, domain objects, and other components.

    ___
    - For example, a `UserController` class can handle user requests, validate inputs, interact with the `User` domain object, and coordinate the overall user-related functionality.
    ___
1. **Pure Fabrication**:

    - The Pure Fabrication principle suggests creating additional classes that do not represent real-world concepts but serve as helpers or utilities to distribute responsibilities and improve system design.

    - These fabricated classes help achieve high cohesion and low coupling.
    ___
    - For example, a `Logger` class can be created as a pure fabrication to handle logging functionality throughout the system.
    ___

1. Indirection:

    - The Indirection principle encourages the use of intermediate classes or interfaces to decouple classes and provide flexibility.

    - It helps in achieving low coupling and extensibility.
    ___
    - For example, a `PaymentProcessor` class can utilize an intermediate `PaymentValidationService` class to perform payment validation before processing the payment.
    ___

1. **Protected Variation**:

    - The Protected Variation principle states that classes should be designed in a way that protects them from changes or variations in other parts of the system.

    - This principle aims to isolate the impact of changes and variations, making the system more adaptable.
    ___
    - For example, an `EmailSender` class can be designed to use an abstract `NotificationProvider` interface, allowing different email service providers to be easily integrated without affecting the `EmailSender` class.
    ___

___

These **GRASP** _principles_ provide guidance for making responsible and effective decisions when assigning responsibilities in object-oriented design. By applying these principles, you can create a well-structured, maintainable, and flexible system.

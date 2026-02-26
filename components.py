from mini_django import jsx
from mini_django import ng_component

@ng_component
def UsersPage():
    users = ["Ada", "Linus", "Grace"]

    return """
    <div>
        <h1>Users</h1>

        <ul>
            <li *ngFor="let user of users">
                {{ user }}
            </li>
        </ul>
        <p *ngIf="showMessage">Hello</p>
    </div>
    """

@jsx
def HomePage():
    return """
    <div className="container">
        <h1>Hello from JSX!</h1>
        <Counter />
    </div>
    """

import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  email = '';
  password = '';
  rememberMe = false;
  showPassword = false;
  errorMessage = '';
  isLoading = false;
  private apiUrl = 'http://127.0.0.1:5001/api/login';

  constructor(
    private http: HttpClient,
    private router: Router
  ) {}

  togglePassword() {
    this.showPassword = !this.showPassword;
  }

  login() {
    this.errorMessage = '';

    if (!this.email || !this.password) {
      this.errorMessage = 'Please enter email and password';
      return;
    }

    this.isLoading = true;

    this.http.post<any>(this.apiUrl, {
      email: this.email.trim(),
      password: this.password
    }).subscribe({
      next: (response) => {
        this.isLoading = false;

        if (response.status === 'success') {
          const storage = this.rememberMe
            ? localStorage
            : sessionStorage;

          storage.setItem('authToken', response.token);
          storage.setItem('currentUser', JSON.stringify(response.user));

          this.router.navigateByUrl('/dashboard');
        } else {
          this.errorMessage = response.message || 'Login failed';
        }
      },
      error: (error) => {
        this.isLoading = false;

        this.errorMessage =
          error.error?.message ||
          'Unable to connect to server. Please try again.';
      }
    });
  }
}



import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterOutlet, NavigationEnd } from '@angular/router';
import { filter, Subscription } from 'rxjs';

import { SidebarComponent } from './layout/sidebar/sidebar.component';
import { HeaderComponent } from './layout/header/header.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,
    SidebarComponent,
    HeaderComponent
  ],
  template: `
    <ng-container *ngIf="!isLoginPage; else loginLayout">
      <div class="app-layout">
        <app-sidebar></app-sidebar>

        <main class="main-content">
          <app-header></app-header>

          <section class="page-content">

            <button
              *ngIf="showBackButton"
              class="global-back-btn"
              (click)="goBack()">
              ← Back
            </button>

            <router-outlet></router-outlet>
          </section>
        </main>
      </div>
    </ng-container>

    <ng-template #loginLayout>
      <router-outlet></router-outlet>
    </ng-template>
  `,
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {

  isLoginPage = true;
  showBackButton = false;

  private routerSubscription?: Subscription;

  constructor(private router: Router) {}

  ngOnInit(): void {
    this.updateLayout(this.router.url);

    this.routerSubscription = this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe((event: any) => {
        this.updateLayout(event.urlAfterRedirects);
      });
  }

  private updateLayout(url: string): void {
    this.isLoginPage = url.startsWith('/login');

    const currentPath = url.split('?')[0].replace(/\/$/, '');

    this.showBackButton =
      !this.isLoginPage &&
      currentPath !== '/dashboard' &&
      currentPath !== '';
  }

  goBack(): void {
    if (window.history.length > 1) {
      window.history.back();
    } else {
      this.router.navigateByUrl('/dashboard');
    }
  }

  ngOnDestroy(): void {
    this.routerSubscription?.unsubscribe();
  }
}

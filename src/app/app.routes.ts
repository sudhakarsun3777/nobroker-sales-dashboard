
import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  },
  {
    path: 'login',
    loadComponent: () =>
      import('./pages/login/login.component')
        .then(m => m.LoginComponent)
  },
  {
    path: 'dashboard',
    loadComponent: () =>
      import('./pages/dashboard/dashboard.component')
        .then(m => m.DashboardComponent)
  },
  {
    path: 'team-performance',
    loadComponent: () =>
      import('./pages/team-performance/team-performance.component')
        .then(m => m.TeamPerformanceComponent)
  },
  {
    path: 'visit-tracking',
    loadComponent: () =>
      import('./pages/visit-tracking/visit-tracking.component')
        .then(m => m.VisitTrackingComponent)
  },
  {
    path: 'schedules',
    loadComponent: () =>
      import('./pages/schedules/schedules.component')
        .then(m => m.SchedulesComponent)
  },
  {
    path: 'revenue',
    loadComponent: () =>
      import('./pages/revenue/revenue.component')
        .then(m => m.RevenueComponent)
  },
  {
    path: 'monthly-reports',
    loadComponent: () =>
      import('./pages/monthly-reports/monthly-reports.component')
        .then(m => m.MonthlyReportsComponent)
  },
  {
    path: 'rm-performance',
    loadComponent: () =>
      import('./pages/rm-performance/rm-performance.component')
        .then(m => m.RmPerformanceComponent)
  },
  {
    path: '**',
    redirectTo: 'login'
  }
];

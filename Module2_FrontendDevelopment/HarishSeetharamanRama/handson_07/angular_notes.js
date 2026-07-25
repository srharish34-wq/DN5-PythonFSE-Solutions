// ============================================================
// Hands-On 7 — Angular: Components, Services, Routing & Forms
// Cognizant DN5.0 | Harish Seetharaman Rama
//
// SETUP:
//   npm install -g @angular/cli
//   ng new student-portal-angular --routing --style=css
//   cd student-portal-angular && ng serve
//
// GENERATE:
//   ng generate component header
//   ng generate component course-list
//   ng generate component course-card
//   ng generate component student-profile
//   ng generate service course
// ============================================================


// ── course.service.ts ──────────────────────────────────────
/*
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({ providedIn: 'root' })   // singleton — shared across whole app
export class CourseService {
  private apiUrl = 'https://jsonplaceholder.typicode.com/posts?_limit=5';

  // Inject HttpClient via constructor (Dependency Injection)
  constructor(private http: HttpClient) {}

  getCourses(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl).pipe(
      map(posts => posts.map((post, i) => ({
        id     : post.id,
        name   : ['Data Structures','DBMS','OOP','Web Dev','Python Backend'][i],
        code   : ['CS101','CS102','CS103','CS104','CS105'][i],
        credits: [4,3,4,3,4][i],
        grade  : ['A','B','A','B','A'][i],
      })))
    );
  }
}
*/


// ── course-list.component.ts ──────────────────────────────
/*
import { Component, OnInit, OnDestroy } from '@angular/core';
import { CourseService } from '../course.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-course-list',
  templateUrl: './course-list.component.html',
  styleUrls: ['./course-list.component.css']
})
export class CourseListComponent implements OnInit, OnDestroy {
  courses: any[]    = [];
  searchTerm: string = '';
  loading: boolean   = true;

  private sub!: Subscription;

  // Inject CourseService via constructor (DI)
  constructor(private courseService: CourseService) {}

  ngOnInit(): void {
    this.sub = this.courseService.getCourses().subscribe({
      next : (data) => { this.courses = data; this.loading = false; },
      error: (err)  => { console.error(err); this.loading = false; }
    });
  }

  // Computed getter for filtered courses
  get filteredCourses() {
    return this.courses.filter(c =>
      c.name.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  // Always unsubscribe to prevent memory leaks
  ngOnDestroy(): void {
    this.sub?.unsubscribe();
  }
}
*/


// ── course-list.component.html ────────────────────────────
/*
<div class="course-list">
  <h2>Available Courses</h2>

  <!-- Two-way binding with ngModel -->
  <input [(ngModel)]="searchTerm" placeholder="Search courses..." />

  <!-- Loading spinner -->
  <div *ngIf="loading" class="spinner">Loading courses...</div>

  <!-- Course cards using *ngFor -->
  <div class="course-grid">
    <app-course-card
      *ngFor="let course of filteredCourses; trackBy: trackById"
      [name]="course.name"
      [code]="course.code"
      [credits]="course.credits"
      [grade]="course.grade">
    </app-course-card>
  </div>

  <!-- *ngIf for empty state -->
  <p *ngIf="filteredCourses.length === 0 && !loading">No courses found.</p>
</div>
*/


// ── course-card.component.ts ──────────────────────────────
/*
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-course-card',
  template: `
    <article class="course-card">
      <h3>{{ name }}</h3>
      <p>{{ code }} | {{ credits }} Credits</p>
      <span class="grade">Grade: {{ grade }}</span>
    </article>
  `
})
export class CourseCardComponent {
  @Input() name!: string;
  @Input() code!: string;
  @Input() credits!: number;
  @Input() grade!: string;
}
*/


// ── student-profile.component.ts — Reactive Forms ─────────
/*
import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-student-profile',
  templateUrl: './student-profile.component.html'
})
export class StudentProfileComponent {
  profileForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.profileForm = this.fb.group({
      name    : ['', Validators.required],
      email   : ['', [Validators.required, Validators.email]],
      semester: ['', [Validators.required, Validators.min(1), Validators.max(8)]]
    });
  }

  onSubmit() {
    if (this.profileForm.valid) {
      console.log('Profile submitted:', this.profileForm.value);
    }
  }
}
*/


// ── student-profile.component.html ───────────────────────
/*
<form [formGroup]="profileForm" (ngSubmit)="onSubmit()">
  <h2>Student Profile</h2>

  <div>
    <label for="name">Full Name</label>
    <input id="name" formControlName="name" placeholder="Enter your name" />
    <span *ngIf="profileForm.get('name')?.touched && profileForm.get('name')?.invalid">
      Name is required
    </span>
  </div>

  <div>
    <label for="email">Email</label>
    <input id="email" type="email" formControlName="email" />
    <span *ngIf="profileForm.get('email')?.touched && profileForm.get('email')?.invalid">
      Enter a valid email
    </span>
  </div>

  <div>
    <label for="semester">Semester (1-8)</label>
    <input id="semester" type="number" formControlName="semester" />
    <span *ngIf="profileForm.get('semester')?.touched && profileForm.get('semester')?.invalid">
      Enter semester between 1 and 8
    </span>
  </div>

  <!-- Disabled until all fields are valid -->
  <button type="submit" [disabled]="profileForm.invalid">Save Profile</button>
</form>
*/


// ── app-routing.module.ts ─────────────────────────────────
/*
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CourseListComponent }    from './course-list/course-list.component';
import { StudentProfileComponent } from './student-profile/student-profile.component';

const routes: Routes = [
  { path: '',        component: CourseListComponent },
  { path: 'profile', component: StudentProfileComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
*/


// ── app.component.html ─────────────────────────────────────
/*
<app-header></app-header>

<nav>
  <a [routerLink]="['/']">Courses</a>
  <a [routerLink]="['/profile']">Profile</a>
</nav>

<!-- Route outlet — renders current route's component -->
<router-outlet></router-outlet>
*/

// NOTE: To run this hands-on:
// 1. Run setup commands above
// 2. Copy each block above into the correct generated file
// 3. ng serve → open http://localhost:4200
console.log('Hands-On 7: Angular — see comments for full implementation');

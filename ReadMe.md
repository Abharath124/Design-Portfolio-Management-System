## Project: Design Portfolio Management System

Build a full-stack portfolio management system for designers to showcase their work.

### Technology Stack (Your Choice)

**Frontend** - Choose ONE:
- React (Vite or Create React App)
- Angular
- HTML + CSS + JavaScript

**Backend** - Choose ONE:
- Java Spring Boot
- Node.js + Express
- Python (Django/Flask)

**Database** - Choose ANY:
- MySQL, PostgreSQL, MongoDB, or any other database

---

## Requirements

### Core Features
1.  **Create Project** - Add portfolio projects with images
2.  **View Projects** - Display project gallery
3.  **Update Project** - Edit project details
4.  **Delete Project** - Remove projects
5.  **Filter** - Filter by category, tools, or year
6.  **Search** - Search projects by name or tags

### Project Data Model
{
  id: auto-generated,
  title: required,
  description: required,
  category: UI Design/UX Design/Web Design/Mobile Design,
  tools: array of strings (Figma, Adobe XD, etc.),
  imageUrls: array of strings,
  projectUrl: string,
  clientName: string,
  completionYear: number,
  tags: array of strings,
  isFeatured: boolean,
  createdAt: timestamp,
  updatedAt: timestamp
}
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects` | Get all projects |
| GET | `/api/projects/:id` | Get single project |
| POST | `/api/projects` | Create new project |
| PUT | `/api/projects/:id` | Update project |
| DELETE | `/api/projects/:id` | Delete project |

---

## UI Pages

1. **Portfolio Gallery** - Grid view of projects
2. **Project Details** - Full project showcase
3. **Add/Edit Project Form** - Manage projects
4. **Filter & Search** - Find specific projects
5. **Admin Dashboard** - Project management

---

## Time Limit

**Duration: 2 Hours**

Complete as much as you can within 2 hours. Focus on:
- Core CRUD functionality first
- Basic UI implementation
- Working API endpoints
- Essential features over polish

**Important Instructions:**
- **Complete working features, not incomplete pieces** - Build complete end-to-end functionality for at least one feature rather than incomplete parts across the entire application
- **Focus on your strengths** - If you are strong in UI/frontend, you can perfect that side and keep the backend simple. If you excel at API/backend development, focus on building a robust API with basic UI
- **Working flow over completeness** - A fully working Create + Read operation is better than incomplete CRUD across all features
- **Quality over quantity** - One well-implemented feature is more valuable than multiple half-finished features

---

## Deliverables

1. Complete source code (backend + frontend)
2. Database schema and sample data
3. API documentation
4. README with setup instructions
5. Screenshots

---

## Evaluation

- **Functionality** (40%) - All CRUD operations work
- **Code Quality** (25%) - Clean, organized code
- **UI/UX** (20%) - Responsive design
- **API Design** (15%) - RESTful principles

## Run Project

1. Clone the repository
2. Install dependencies
3. Run the backend server 
    python app.py
4. Run the frontend server 
    python -m http.server 5500
5. Open the frontend in your browser

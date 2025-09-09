import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import BodyView from '@/layout/BodyView.vue';
import AuthView from '@/components/common/block/auth/AuthView.vue';
import LoginPage from '@/components/common/block/auth/LoginPage.vue';
import indexHome from '@/pages/dashbords/indexHome.vue';
import indexZentra from '@/pages/dashbords/indexZentra.vue';
import indexBarani from '@/pages/dashbords/indexBarani.vue';
import indexHydromet from '@/pages/dashbords/indexHydromet.vue';
import indexPaws from '@/pages/dashbords/indexPaws.vue';
import indexWeatherStations from '@/pages/dashbords/indexWeatherStations.vue';
import indexSutron from '@/pages/dashbords/indexSutron.vue';
import indexCreateProject from '@/pages/dashbords/indexCreateProject.vue';
import indexProfile from '@/pages/user/indexProfile.vue';
import indexEdit from '@/pages/user/indexEdit.vue';
import indexKnowledgebase from '@/pages/faq/indexFaq.vue';
import indexAPI from '@/pages/api/indexAPI.vue';
import indexUserManagement from '@/pages/users_management/indexUserManagement.vue';
import indexCreateUser from '@/pages/createuser/indexCreateUser.vue';
import indexStationManagement from '@/pages/station_management/indexStationManagement.vue';
import indexApiKeyUsageLogs from '@/pages/api/indexApiKeyUsageLogs.vue';

import { useAuthStore } from '@/store/auth';
import { useChatStore } from '@/store/chat';
import indexBrands from '@/pages/dashbords/indexBrands.vue';
import indexPrivateChat from '@/pages/chat/indexPrivateChat.vue';

// import demoRoutes from './demos';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/auth/login',
    name: 'Login',
    component: () => import('@/components/common/block/auth/LoginPage.vue'),
    meta: {
      requiresAuth: false
    }
  },
  {
    path: '',
    redirect: '/dashboard'
  },
  {
    path: '/',
    name: 'home',
    component: BodyView,
    meta: {
      title: 'Meteorological Data Processing System',
    },
    children: [
      {
        path: '',
        name: 'defaultRoot',
        component: indexHome,
        meta: {
          title: 'Meteorological Data Processing System',
        }
      }
    ]
  },
  {
    path: '/auth',
    component: AuthView,
    children: [
      {
        path: 'login',
        name: 'login',
        component: LoginPage,
        meta: {
          title: 'Meteorological Data Processing System',
          requiresAuth: false
        }
      }
    ]
  },
  {
    path: '/dashboard',
    component: BodyView,
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: indexHome,
        meta: {
          title: 'Dashboards | MDPS',
          requiresAuth: true
        }
      },
    ]
  },

  {
    path: '/brands',
    component: BodyView,
    children: [
      {
        path: '',
        name: 'WeatherStationBrands',
        component: indexBrands,
        meta: {
          title: 'Weather Station Brands | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'create',
        name: 'createProject',
        component: indexCreateProject,
        meta: {
          title: 'Create Project| MDPS',
          requiresAuth: true
        }
      },
    ]
  },

  {
    path: '/stations',
    component: BodyView,
    children: [
      {
        path: '',
        name: 'WeatherStations',
        component: indexWeatherStations,
        meta: {
          title: 'Weather Stations | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'create',
        name: 'createProject',
        component: indexCreateProject,
        meta: {
          title: 'Create Project| MDPS',
          requiresAuth: true
        }
      },

      {
        path: 'AWS_Barani',
        name: 'Barani',
        component: indexBarani,
        meta: {
          title: 'Dashboards Education | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'AWS_3D_Paws',
        name: '3DPaws',
        component: indexPaws,
        meta: {
          title: 'Dashboards Education | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'AWS_OTT_Hyrdomet',
        name: 'OTT Hydromet',
        component: indexHydromet,
        meta: {
          title: 'Dashboards Education | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'AWS_Zentra',
        name: 'Zentra',
        component: indexZentra,
        meta: {
          title: 'Dashboards Education | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'AWS_Sutron',
        name: 'Sutron',
        component: indexSutron,
        meta: {
          title: 'Sutron Weather Stations | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'manage',
        name: 'Manage Stations',
        component: indexStationManagement,
        meta: {
          title: 'Manage Stations | MDPS',
          requiresAuth: true,
          requiresAdmin: true
        }
      },
      {
        path: 'management/createstation',
        name: 'Create Station',
        component: () => import('@/pages/station_management/createstation.vue'),
        meta: {
          requiresAuth: true,
          title: 'Create Station | MDPS'
        }
      },
    ]
  },

  // {
  //   path: '/',
  //   component: BodyView,
  //   children: [
  //     {
  //       path: 'project_list',
  //       name: 'projectList',
  //       component: indexProjectlist,
  //       meta: {
  //         title: 'Project List | MDPS',
  //         requiresAuth: true
  //       }
  //     },
  //
  //   ]
  // },

  {
    path: '/support',
    component: BodyView,
    children: [
      // {
      //   path: 'file_manager',
      //   name: 'fileManager',
      //   component: indexFileManeger,
      //   meta: {
      //     title: 'File Manager | MDPS',
      //     requiresAuth: true
      //   }
      // },
      // {
      //   path: 'kanban_board',
      //   name: 'kanbanBoard',
      //   component: indexKanbanBoard,
      //   meta: {
      //     title: 'Kanban Board | MDPS',
      //     requiresAuth: true
      //   }
      // },
      // {
      //   path: 'letter_box',
      //   name: 'letterbox',
      //   component: indexLetterBox,
      //   meta: {
      //     title: 'Letter Box| MDPS',
      //     requiresAuth: true
      //   }
      // },
      {
        path: 'chat',
        name: 'Chatapp',
        component: indexPrivateChat,
        meta: {
          title: 'Private Chat| MDPS',
          requiresAuth: true
        }
      },
      // {
      //   path: 'group_chat',
      //   name: 'Group Chat',
      //   component: indexGroupChat,
      //   meta: {
      //     title: 'Group Chat| MDPS',
      //     requiresAuth: true
      //   }
      // },
      // {
      //   path: 'bookmark',
      //   name: 'bookmark',
      //   component: indexBookmark,
      //   meta: {
      //     title: 'Bookmark| MDPS',
      //     requiresAuth: true
      //   }
      // },
      // {
      //   path: 'contact',
      //   name: 'contacts',
      //   component: indexContact,
      //   meta: {
      //     title: 'contact| MDPS',
      //     requiresAuth: true
      //   }
      // },
      // {
      //   path: 'todo',
      //   name: 'todo',
      //   component: indexTodo,
      //   meta: {
      //     title: 'To Do| MDPS',
      //     requiresAuth: true
      //   }
      // },
      // {
      //   path: 'task',
      //   name: 'task',
      //   component: indexTask,
      //   meta: {
      //     title: 'Task| MDPS',
      //     requiresAuth: true
      //   }
      // },
      // {
      //   path: 'calendar',
      //   name: 'calendar',
      //   component: indexCalendar,
      //   meta: {
      //     title: 'Calendar| MDPS',
      //     requiresAuth: true
      //   }
      // }

    ]
  },

  {
    path: '/users',
    component: BodyView,
    children: [
      {
        path: '',
        name: 'Users Management',
        component: indexUserManagement,
        meta: {
          title: 'Support | MDPS',
          requiresAuth: true,
          requiresAdmin: true
        }
      },
      {
        path: 'create',
        name: 'Create User',
        component: indexCreateUser,
        meta: {
          requiresAuth: true,
          title: 'Create User | MDPS'
        }
      },
      {
        path: 'profile',
        name: 'userProfile',
        component: indexProfile,
        meta: {
          title: 'User Profile| MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'edit',
        name: 'indexEdit',
        component: indexEdit,
        meta: {
          title: 'User Edit| MDPS',
          requiresAuth: true
        }
      },
      // {
      //   path: 'cards',
      //   name: 'usercard',
      //   component: indexCard,
      //   meta: {
      //     title: 'User Cards| MDPS',
      //     requiresAuth: true
      //   }
      // }
    ]
  },

  {
    path: '/pages',
    component: BodyView,
    children: [
      // {
      //   path: 'users_management',
      //   name: 'Users Management',
      //   component: indexUserManagement,
      //   meta: {
      //     title: 'Support | MDPS',
      //     requiresAuth: true,
      //     requiresAdmin: true
      //   }
      // },
      // {
      //   path: 'users_management/createuser',
      //   name: 'Create Users',
      //   component: indexCreateUser,
      //   meta: {
      //     requiresAuth: true,
      //     title: 'Create User | MDPS'
      //   }
      // },
      {
        path: 'knowledgebase',
        name: 'knowledgebase',
        component: indexKnowledgebase,
        meta: {
          title: 'Knowledge Base | Documentation',
          requiresAuth: true
        }
      }
    ]
  },

  {
    path: '/api',
    component: BodyView,
    children: [
      {
        path: 'keys',
        name: 'API Management',
        component: indexAPI,
        meta: {
          title: 'Support | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'indexAPI',
        name: 'indexAPI',
        component: indexAPI,
        meta: {
          title: 'API Management | MDPS',
          requiresAuth: true
        }
      },
      {
        path: 'usage-logs/:uuid',
        name: 'apiKeyUsageLogs',
        component: indexApiKeyUsageLogs,
        props: true,
        meta: {
          title: 'API Key Usage Logs | MDPS',
          requiresAuth: true
        }
      },
    ]
  },
  // {
  //   path: '/users_management',
  //   component: BodyView,
  //   meta: {
  //     requiresAuth: true,
  //     requiresAdmin: true
  //   },
  //   beforeEnter: async (to, from, next) => {
  //     console.log('Entering users_management route guard');
  //     const authStore = useAuthStore();
  //     const { checkAuth, isAdmin } = authStore;
  //     await checkAuth();
  //
  //     if (!isAdmin) {
  //       next({ path: '/dashboard' });
  //     } else {
  //       next();
  //     }
  //   },
  //   children: [
  //     {
  //       path: '',
  //       name: 'UserManagement',
  //       component: () => import('@/pages/users_management/indexUserManagement.vue'),
  //       meta: {
  //         requiresAdmin: true
  //       }
  //     },
  //     {
  //       path: 'createuser',
  //       name: 'CreateUser',
  //       component: () => import('@/pages/createuser/indexCreateUser.vue'),
  //       meta: {
  //         requiresAdmin: true
  //       }
  //     }
  //   ]
  // },
  // {
  //   path: '/dashboards/Main_Dashboard',
  //   name: 'MainDashboard',
  //   component: () => import('@/pages/dashbords/indexHome.vue'),
  //   meta: {
  //     requiresAuth: true,
  //     title: 'Main Dashboard'
  //   }
  // },
  // {
  //   path: '/dashboards/station_status',
  //   name: 'StationStatus',
  //   component: () => import('@/pages/dashbords/indexStationStatus.vue'),
  //   meta: {
  //     requiresAuth: true,
  //     title: 'Station Status | MDPS'
  //   }
  // },

  // ...demoRoutes
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach(async (to, from, next) => {
  // Set document title based on route meta
  if (to.meta.title) {
    document.title = to.meta.title as string;
  } else {
    document.title = 'MDPS';
  }

  const authStore = useAuthStore();
  const { checkAuth, isAdmin, isStaff, currentUser } = authStore;
  const chatStore = useChatStore();

  // Allow access to login page without authentication
  if (to.path === '/auth/login') {
    if (!currentUser) {
      const isAuthenticated = await checkAuth();
      if (isAuthenticated) {
        next('/');
        return;
      }
    }
    next();
    return;
  }

  // Check authentication for protected routes
  let isAuthenticated = true;
  if (!currentUser) {
    isAuthenticated = await checkAuth();
  }
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/auth/login');
    return;
  }

  // Check admin requirement
  if (to.matched.some(record => record.meta.requiresAdmin) && !isAdmin) {
    next({ path: '/dashboard' });
    return;
  }

  // Only initialize chat on chat-related routes
  if (to.path.includes('/chat') || to.path.includes('/messages')) {
    chatStore.setInChatRoute(true);
  } else {
    chatStore.setInChatRoute(false);
    // Clear any polling intervals
    if (chatStore.presencePollingInterval) {
      clearInterval(chatStore.presencePollingInterval);
    }
    if (chatStore.messagePollingInterval) {
      clearInterval(chatStore.messagePollingInterval);
    }
  }

  next();
});

export default router;

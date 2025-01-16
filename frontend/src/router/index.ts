import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import BodyView from "@/layout/BodyView.vue"
import AuthView from "@/components/common/block/auth/AuthView.vue"
import LoginPage from "@/components/common/block/auth/LoginPage.vue"
import indexHome from "@/pages/dashbords/indexHome.vue"
import indexProject from "@/pages/dashbords/indexProject.vue"
import indexEcommerce from "@/pages/dashbords/indexEcommerce.vue"
import indexZentra from "@/pages/dashbords/indexZentra.vue"
import indexBarani from "@/pages/dashbords/indexBarani.vue"
import indexHydromet from "@/pages/dashbords/indexHydromet.vue"
import indexSutron from "@/pages/dashbords/indexSutron.vue"
import indexPaws from "@/pages/dashbords/indexPaws.vue"
import indexGeneral from "@/pages/widgets/indexGeneral.vue"
import indexChart from "@/pages/widgets/indexChart.vue"
import indexProjectlist from "@/pages/project/indexProjectlist.vue"
import indexCreateProject from "@/pages/dashbords/indexCreateProject.vue"
import indexFileManeger from "@/pages/filemaneger/indexFileManeger.vue"
import indexKanbanBoard from "@/pages/kanban/indexKanbanBoard.vue"
import indexAddProduct from "@/pages/ecommerce/indexAddProduct.vue"
import indexProduct from "@/pages/ecommerce/indexProduct.vue"
import indexCart from "@/pages/ecommerce/indexCart.vue"
import indexProductPage from "@/pages/ecommerce/indexProductPage.vue"
import indexCheckout from "@/pages/ecommerce/indexCheckout.vue"
import indexPaymentDetail from "@/pages/ecommerce/indexPaymentDetail.vue"
import indexOrder from "@/pages/ecommerce/indexOrder.vue"
import indexWishlist from "@/pages/ecommerce/indexWishlist.vue"
import indexPricing from "@/pages/ecommerce/indexPricing.vue"
import indexInvoiceOne from "@/pages/ecommerce/indexInvoiceOne.vue"
import indexProductList from "@/pages/ecommerce/indexProductList.vue"
import indexInvoiceTwo from "@/pages/ecommerce/indexInvoiceTwo.vue"
import indexInvoiceThree from "@/pages/ecommerce/indexInvoiceThree.vue"
import indexInvoiceFour from "@/pages/ecommerce/indexInvoiceFour.vue"
import indexInvoiceFive from "@/pages/ecommerce/indexInvoiceFive.vue"
import indexInvoiceSix from "@/pages/ecommerce/indexInvoiceSix.vue"
import indexLetterBox from "@/pages/letterbox/indexLetterBox.vue"
import indexPrivateChat from "@/pages/chat/indexPrivateChat.vue"
import indexGroupChat from "@/pages/chat/indexGroupChat.vue"
import indexProfile from "@/pages/user/indexProfile.vue"
import indexEdit from "@/pages/user/indexEdit.vue"
import indexCard from "@/pages/user/indexCard.vue"
import indexBookmark from "@/pages/bookmark/indexBookmark.vue"
import indexContact from "@/pages/contacts/indexContact.vue"
import indexTask from "@/pages/task/indexTask.vue"
import indexCalendar from "@/pages/calendar/indexCalendar.vue"
import indexSoical from "@/pages/socialapp/indexSoical.vue"
import indexTodo from "@/pages/todo/indexTodo.vue"
import indexSearch from "@/pages/search/indexSearch.vue"
import indexValidation from "@/pages/forms/formcontrols/indexValidation.vue"
import indexInputs from "@/pages/forms/formcontrols/indexInputs.vue"
import indexCheckbox from "@/pages/forms/formcontrols/indexCheckbox.vue"
import indexGroups from "@/pages/forms/formcontrols/indexGroups.vue"
import indexMask from "@/pages/forms/formcontrols/indexMask.vue"
import indexMega from "@/pages/forms/formcontrols/indexMega.vue"
import indexDatapicker from "@/pages/forms/formwidgets/indexDatapicker.vue"
import indexTouchspin from "@/pages/forms/formwidgets/indexTouchspin.vue"
import indexSelect from "@/pages/forms/formwidgets/indexSelect.vue"
import indexTypeahead from "@/pages/forms/formwidgets/indexTypeahead.vue"
import indexClipboard from "@/pages/forms/formwidgets/indexClipboard.vue"
import indexSwitch from "@/pages/forms/formwidgets/indexSwitch.vue"
import formWizard from "@/pages/forms/formlayout/formWizard.vue"
import formWizard2 from "@/pages/forms/formlayout/formWizard2.vue"
import indexTwofactor from "@/pages/forms/formlayout/indexTwofactor.vue"
import indexBootstrap from "@/pages/table/indexBootstrap.vue"
import indexComponent from "@/pages/table/indexComponent.vue"
import indexInit from "@/pages/table/indexInit.vue"
import indexTypography from "@/pages/uikits/indexTypography.vue"
import indexAvatars from "@/pages/uikits/indexAvatars.vue"
import indexHelper from "@/pages/uikits/indexHelper.vue"
import indexGrid from "@/pages/uikits/indexGrid.vue"
import indexTagPills from "@/pages/uikits/indexTagPills.vue"
import indexProgress from "@/pages/uikits/indexProgress.vue"
import indexModal from "@/pages/uikits/indexModal.vue"
import indexAlert from "@/pages/uikits/indexAlert.vue"
import indexPopover from "@/pages/uikits/indexPopover.vue"
import indexTooltip from "@/pages/uikits/indexTooltip.vue"
import indexDropdown from "@/pages/uikits/indexDropdown.vue"
import indexAccordion from "@/pages/uikits/indexAccordion.vue"
import indexTabs from "@/pages/uikits/indexTabs.vue"
import indexLists from "@/pages/uikits/indexLists.vue"
import indexAnimate from "@/pages/animation/indexAnimate.vue"
import indexAos from "@/pages/animation/indexAos.vue"
import indexFlag from "@/pages/icons/indexFlag.vue"
import indexFontawesome from "@/pages/icons/indexFontawesome.vue"
import indexThemify from "@/pages/icons/indexThemify.vue"
import indexIcoicon from "@/pages/icons/indexIcoicon.vue"
import indexFeather from "@/pages/icons/indexFeather.vue"
import indexWhether from "@/pages/icons/indexWhether.vue"
import indexDefaultStyle from "@/pages/buttons/indexDefaultStyle.vue"
import indexFlat from "@/pages/buttons/indexFlat.vue"
import indexEdge from "@/pages/buttons/indexEdge.vue"
import indexRaised from "@/pages/buttons/indexRaised.vue"
import indexGroup from "@/pages/buttons/indexGroup.vue"
import indexApexchart from "@/pages/charts/indexApexchart.vue"
import indexGoogle from "@/pages/charts/indexGoogle.vue"
import indexChartist from "@/pages/charts/indexChartist.vue"
import indexSample from "@/pages/samplepage/indexSample.vue"
import indexInternationalization from "@/pages/internationalization/indexInternationalization.vue"
import indexErrorPage1 from "@/pages/error/indexErrorPage1.vue"
import indexErrorPage2 from "@/pages/error/indexErrorPage2.vue"
import indexErrorPage3 from "@/pages/error/indexErrorPage3.vue"
import indexErrorPage4 from "@/pages/error/indexErrorPage4.vue"
import indexErrorPage5 from "@/pages/error/indexErrorPage5.vue"
import indexErrorPage6 from "@/pages/error/indexErrorPage6.vue"
import indexComingsoonPage from "@/pages/comingsoon/indexComingsoonPage.vue"
import indexComingsoonImage from "@/pages/comingsoon/indexComingsoonImage.vue"
import indexComingsoonVideo from "@/pages/comingsoon/indexComingsoonVideo.vue"
import loginSimple from "@/pages/authentication/loginSimple.vue"
import loginImage from "@/pages/authentication/loginImage.vue"
import loginImageTwo from "@/pages/authentication/loginImageTwo.vue"
import loginValidation from "@/pages/authentication/loginValidation.vue"
import loginTooltip from "@/pages/authentication/loginTooltip.vue"
import loginSweetalert from "@/pages/authentication/loginSweetalert.vue"
import registerSimple from "@/pages/authentication/registerSimple.vue"
import registerImage from "@/pages/authentication/registerImage.vue"
import registerImageTwo from "@/pages/authentication/registerImageTwo.vue"
import unlockUser from "@/pages/authentication/unlockUser.vue"
import forgetPassword from "@/pages/authentication/forgetPassword.vue"
import resetPassword from "@/pages/authentication/resetPassword.vue"
import maintenanceView from "@/pages/authentication/maintenanceView.vue"
import indexGallery from "@/pages/gallery/indexGallery.vue"
import indexGriddesc from "@/pages/gallery/indexGriddesc.vue"
import indexMasonry from "@/pages/gallery/indexMasonry.vue"
import indexMasonarydesc from "@/pages/gallery/indexMasonarydesc.vue"
import indexHoverGallery from "@/pages/gallery/indexHoverGallery.vue"
import indexDetails from "@/pages/blog/indexDetails.vue"
import indexSingle from "@/pages/blog/indexSingle.vue"
import indexAdd from "@/pages/blog/indexAdd.vue"
import indexFaq from "@/pages/faq/indexFaq.vue"
import indexJobCard from "@/pages/job/indexCard.vue"
import indexList from "@/pages/job/indexList.vue"
import indexJobDetails from "@/pages/job/indexDetails.vue"
import indexApply from "@/pages/job/indexApply.vue"
import indexLearning from "@/pages/learning/indexLearning.vue"
import indexGoogleMap from "@/pages/maps/indexGoogle.vue"
import indexCourse from "@/pages/learning/indexCourse.vue"
import indexLeaflet from "@/pages/maps/indexLeaflet.vue"
import indexCk from "@/pages/editor/indexCk.vue"
import simpleEditor from "@/pages/editor/simpleEditor.vue"
import indexKnowledgebase from "@/pages/knowledgebase/indexKnowledgebase.vue"
import indexAPI from "@/pages/api/indexAPI.vue"
import indexUserManagement from "@/pages/users_management/indexUserManagement.vue"
import indexCreateUser from "@/pages/createuser/indexCreateUser.vue"
import indexScrollable from "@/pages/advance/indexScrollable.vue"
import indexTree from "@/pages/advance/indexTree.vue"
import indexToasts from "@/pages/advance/indexToasts.vue"
import indexRating from "@/pages/advance/indexRating.vue"
import indexDropzone from "@/pages/advance/indexDropzone.vue"
import indexTour from "@/pages/advance/indexTour.vue"
import indexSweetalert from "@/pages/advance/indexSweetalert.vue"
import animationModal from "@/pages/advance/animationModal.vue"
import owlCarousel from "@/pages/advance/owlCarousel.vue"
import indexCropper from "@/pages/advance/indexCropper.vue"
import indexBasiccard from "@/pages/advance/indexBasiccard.vue"
import indexCreative from "@/pages/advance/indexCreative.vue"
import indexDraggable from "@/pages/advance/indexDraggable.vue"
import indexTimeline from "@/pages/advance/indexTimeline.vue"
import indexRibbon from "@/pages/advance/indexRibbon.vue"
import indexPagenation from "@/pages/advance/indexPagenation.vue"
import indexBreadcrumb from "@/pages/advance/indexBreadcrumb.vue"
import indexRange from "@/pages/advance/indexRange.vue"

import { useAuth } from '@/composables/useAuth'

const routes: Array<RouteRecordRaw> = [
  {
    path: "/auth/login",
    name: "Login",
    component: () => import("@/components/common/block/auth/LoginPage.vue"),
    meta: {
      requiresAuth: false
    }
  },
  {
    path: "",
    redirect: "/dashboards/Main_Dashboard"
  },
  {
    path: '/',
    name: 'home',
    component: BodyView,
    meta: {
      title: 'Mofi - Premium Vue Admin Template',
    },
    children: [
      {
        path: '',
        name: 'defaultRoot',
        component: indexHome,
        meta: {
          title: 'Mofi - Premium Vue Admin Template',
        }
      }
    ]
  },
  {
    path: "/auth",
    component: AuthView,
    children: [
      {
        path: "login",
        name: "login",
        component: LoginPage,
        meta: {
          title: 'Mofi - Premium Vue Admin Template',
          requiresAuth: false
        }
      }
    ]
  },
  {
    path: "/dashboards",
    component: BodyView,
    children: [
      {
        path: "Main_Dashboard",
        name: "Main",
        component: indexHome,
        meta: {
          title: 'Dashboards | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "dashboard_project",
        name: "project",
        component: indexProject,
        meta: {
          title: 'Dashboards CRM | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "dashboard_ecommerce",
        name: "ecommerce",
        component: indexEcommerce,
        meta: {
          title: 'Dashboards Ecommerce | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "Create_New_AWS",
        name: "createProject",
        component: indexCreateProject,
        meta: {
          title: 'Create Project| Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      
    ]
  },

  {
    path: "/stations",
    component: BodyView,
    children: [
 
      {
        path: "AWS_Barani",
        name: "Barani",
        component: indexBarani,
        meta: {
          title: 'Dashboards Education | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "AWS_3D_Paws",
        name: "3DPaws",
        component: indexPaws,
        meta: {
          title: 'Dashboards Education | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "AWS_Sutron",
        name: "Sutron",
        component: indexSutron,
        meta: {
          title: 'Dashboards Education | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "AWS_OTT_Hyrdomet",
        name: "OTT Hydromet",
        component: indexHydromet,
        meta: {
          title: 'Dashboards Education | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "AWS_Zentra",
        name: "Zentra",
        component: indexZentra,
        meta: {
          title: 'Dashboards Education | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
    ]
  },

  {
    path: "/widgets",
    component: BodyView,
    children: [
      {
        path: "general",
        name: "General",
        component: indexGeneral,
        meta: {
          title: 'Widgets General | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "Chart",
        name: "charts",
        component: indexChart,
        meta: {
          title: 'Widgets Chart | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: "/",
    component: BodyView,
    children: [
      {
        path: "project_list",
        name: "projectList",
        component: indexProjectlist,
        meta: {
          title: 'Project List| Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },

    ]
  },
  {
    path: "/app",
    component: BodyView,
    children: [
      {
        path: "file_manager",
        name: "fileManager",
        component: indexFileManeger,
        meta: {
          title: 'File Manager| Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "kanban_board",
        name: "kanbanBoard",
        component: indexKanbanBoard,
        meta: {
          title: 'kanban Board| Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "letter_box",
        name: "letterbox",
        component: indexLetterBox,
        meta: {
          title: 'Letter Box| Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "private_chat",
        name: "Chatapp",
        component: indexPrivateChat,
        meta: {
          title: 'Private Chat| Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "group_chat",
        name: "Group Chat",
        component: indexGroupChat,
        meta: {
          title: 'Group Chat| Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "bookmark",
        name: "bookmark",
        component: indexBookmark,
        meta: {
          title: 'Bookmark| Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "contact",
        name: "contacts",
        component: indexContact,
        meta: {
          title: 'contact| Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "todo",
        name: "todo",
        component: indexTodo,
        meta: {
          title: 'To Do| Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "task",
        name: "task",
        component: indexTask,
        meta: {
          title: 'Task| Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "calendar",
        name: "calendar",
        component: indexCalendar,
        meta: {
          title: 'Calendar| Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      }

    ]
  },
  {
    path: "/ecommerce",
    component: BodyView,
    children: [
      {
        path: "add_product",
        name: "addporduct",
        component: indexAddProduct,
        meta: {
          title: 'Add Product | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "product",
        name: "product",
        component: indexProduct,
        meta: {
          title: 'Product | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "cart",
        name: "cart",
        component: indexCart,
        meta: {
          title: 'Cart | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "details/:id",
        name: "productPage",
        component: indexProductPage,
        meta: {
          title: 'Product Page | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },

      {
        path: "payment_details",
        name: "paymentDetail",
        component: indexPaymentDetail,
        meta: {
          title: 'Payment Detail | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "invoice_1",
        name: "Invoice_1",
        component: indexInvoiceOne,
        meta: {
          title: 'Invoice | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "invoice_2",
        name: "Invoice_2",
        component: indexInvoiceTwo,
        meta: {
          title: 'Invoice Two | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "invoice_3",
        name: "Invoice_3",
        component: indexInvoiceThree,
        meta: {
          title: 'Invoice Three | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "invoice_4",
        name: "Invoice_4",
        component: indexInvoiceFour,
        meta: {
          title: 'Invoice Four | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "invoice_5",
        name: "Invoice_5",
        component: indexInvoiceFive,
        meta: {
          title: 'Invoice Five | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "invoice_6",
        name: "Invoice_6",
        component: indexInvoiceSix,
        meta: {
          title: 'Invoice Six | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "checkout",
        name: "Checkout",
        component: indexCheckout,
        meta: {
          title: 'Checkout | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "pricing",
        name: "pricing",
        component: indexPricing,
        meta: {
          title: 'Pricing | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "wishlist",
        name: "Wishlist",
        component: indexWishlist,
        meta: {
          title: 'Wish List | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "order_history",
        name: "Orderhistory",
        component: indexOrder,
        meta: {
          title: 'Order History | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "product_list",
        name: "productlist",
        component: indexProductList,
        meta: {
          title: 'Product list | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: "/users",
    component: BodyView,
    children: [
      {
        path: "profile",
        name: "userProfile",
        component: indexProfile,
        meta: {
          title: 'User Profile| Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "edit",
        name: "indexEdit",
        component: indexEdit,
        meta: {
          title: 'User Edit| Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "cards",
        name: "usercard",
        component: indexCard,
        meta: {
          title: 'User Cards| Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: "/pages",
    component: BodyView,
    children: [
      {
        path: "social_app",
        name: "socialapp",
        component: indexSoical,
        meta: {
          title: 'Social App| Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "search",
        name: "searchresult",
        component: indexSearch,
        meta: {
          title: 'Search| Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "sample_page",
        name: "samplepage",
        component: indexSample,
        meta: {
          title: 'Simple Page| Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "internationalization",
        name: "Internationalization",
        component: indexInternationalization,
        meta: {
          title: 'Internationalization| Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "faq",
        name: "faq",
        component: indexFaq,
        meta: {
          title: 'Faq| Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "api",
        name: "API Management",
        component: indexAPI,
        meta: {
          title: 'Support | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "users_management",
        name: "Users Management",
        component: indexUserManagement,
        meta: {
          title: 'Support | Mofi - Premium Vue Admin Template',
          requiresAuth: true,
          requiresAdmin: true
        }
      },
      {
        path: "users_management/createuser",
        name: "Create Users",
        component: indexCreateUser,
        meta: {
          requiresAuth: true,
          title: 'Create User | Mofi - Premium Vue Admin Template'
        }
      }
    ]
  },

  {
    path: "/form",
    component: BodyView,
    children: [
      {
        path: "validation",
        name: "formValidation",
        component: indexValidation,
        meta: {
          title: 'Form Controls Form Validation | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "base_inputs",
        name: "indexInputs",
        component: indexInputs,
        meta: {
          title: 'Form Controls Base Input | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "checkbox_radio",
        name: "indexCheckbox",
        component: indexCheckbox,
        meta: {
          title: 'Form Controls Checkbox & Radio | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "select2",
        name: "Select",
        component: indexSelect,
        meta: {
          title: 'Form Widgets Select | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "input_groups",
        name: "indexGroups",
        component: indexGroups,
        meta: {
          title: 'Form Controls Input Groups | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "input_mask",
        name: "indexMask",
        component: indexMask,
        meta: {
          title: 'Form Controls Input Mask | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "mega_options",
        name: "indexMega",
        component: indexMega,
        meta: {
          title: 'Form Controls Mega Options | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "datepicker",
        name: "datapicker",
        component: indexDatapicker,
        meta: {
          title: 'Form Widgets Datepicker | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "touchspin",
        name: "indexTouchspin",
        component: indexTouchspin,
        meta: {
          title: 'Form Widgets Touchspin | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "switch",
        name: "indexSwitch",
        component: indexSwitch,
        meta: {
          title: 'Form Widgets Switch| Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "typeahead",
        name: "indexTypeahead",
        component: indexTypeahead,
        meta: {
          title: 'Form Widgets Typeahead | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "clipboard",
        name: "indexClipboard",
        component: indexClipboard,
        meta: {
          title: 'Form Widgets Clipboard | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "form_wizard_two",
        name: "formWizardtwo",
        component: formWizard2,
        meta: {
          title: 'Form Layout Form Wizard 2 | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "two_actor",
        name: "Two Factor",
        component: indexTwofactor,
        meta: {
          title: 'Form Layout Two Factor| Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "form_wizard",
        name: "formWizard",
        component: formWizard,
        meta: {
          title: 'Form Layout Form Wizard 2| Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
    ]
  },
  {
    path: "/table",
    component: BodyView,
    children: [
      {
        path: "basic",
        name: "bootstrp",
        component: indexBootstrap,
        meta: {
          title: 'Table Bootstrap Table | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "table_components",
        name: "tablecomponent",
        component: indexComponent,
        meta: {
          title: 'Table Table Components | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "datatable_basic",
        name: "basicinit",
        component: indexInit,
        meta: {
          title: 'Table Basic Init | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: "/uikits",
    component: BodyView,
    children: [
      {
        path: "typography",
        name: "Typography",
        component: indexTypography,
        meta: {
          title: 'Uikits Typography | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "avatars",
        name: "Avatars",
        component: indexAvatars,
        meta: {
          title: 'Uikits Avatars | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "helper_classes",
        name: "Helper",
        component: indexHelper,
        meta: {
          title: 'Uikits Helper Classes | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "grid",
        name: "Grid",
        component: indexGrid,
        meta: {
          title: 'Uikits Grid | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "tag_pills",
        name: "TagPills",
        component: indexTagPills,
        meta: {
          title: 'Uikits Tag & Pills | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "progress_bar",
        name: "Progress",
        component: indexProgress,
        meta: {
          title: 'Uikits Progressbar | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "modal",
        name: "model",
        component: indexModal,
        meta: {
          title: 'Uikits Modal | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "alert",
        name: "alert",
        component: indexAlert,
        meta: {
          title: 'Uikits Alert | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "popover",
        name: "popover",
        component: indexPopover,
        meta: {
          title: 'Uikits popover | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "tooltip",
        name: "tooltip",
        component: indexTooltip,
        meta: {
          title: 'Uikits Tooltip | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "dropdown",
        name: "Dropdown",
        component: indexDropdown,
        meta: {
          title: 'Uikits Dropdown | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "accordion",
        name: "Accordion",
        component: indexAccordion,
        meta: {
          title: 'Uikits Accordion | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "tabs",
        name: "Tabs",
        component: indexTabs,
        meta: {
          title: 'Uikits Tabs | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "lists",
        name: "lists",
        component: indexLists,
        meta: {
          title: 'Uikits Lists | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: "/animation",
    component: BodyView,
    children: [
      {
        path: "animate",
        name: "animate",
        component: indexAnimate,
        meta: {
          title: 'Animate | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "aos_animation",
        name: "aos",
        component: indexAos,
        meta: {
          title: 'Aos Animation | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: "/icons",
    component: BodyView,
    children: [
      {
        path: "flag",
        name: "flag",
        component: indexFlag,
        meta: {
          title: 'Icons Flag | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "fontawesome",
        name: "Fontawesome",
        component: indexFontawesome,
        meta: {
          title: 'Icons Fontawesome | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "themify",
        name: "Themify",
        component: indexThemify,
        meta: {
          title: 'Icons Themify | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "feather_icon",
        name: "Feather",
        component: indexFeather,
        meta: {
          title: 'Icons Feather | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "whether",
        name: "indexWether",
        component: indexWhether,
        meta: {
          title: 'Icons Whether | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "ico",
        name: "Icoicon",
        component: indexIcoicon,
        meta: {
          title: 'Icons Icoicon | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: "/buttons",
    component: BodyView,
    children: [
      {
        path: "default_button",
        name: "button",
        component: indexDefaultStyle,
        meta: {
          title: 'Buttons Default | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "flat",
        name: "Flat",
        component: indexFlat,
        meta: {
          title: 'Buttons Flat | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "edge",
        name: "Edge",
        component: indexEdge,
        meta: {
          title: 'Buttons Edge | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "raised",
        name: "Raised",
        component: indexRaised,
        meta: {
          title: 'Buttons Raised | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "group",
        name: "Group",
        component: indexGroup,
        meta: {
          title: 'Buttons Group | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },

    ]
  },
  {
    path: "/chart",
    component: BodyView,
    children: [
      {
        path: "apexChart",
        name: "Apexchart",
        component: indexApexchart,
        meta: {
          title: 'Chart Apex Chart | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "google",
        name: "google",
        component: indexGoogle,
        meta: {
          title: 'Chart Google Chart | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "chartist",
        name: "chartist",
        component: indexChartist,
        meta: {
          title: 'Chart Chartist Chart | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: "/error_page1",
    name: "errorPage1",
    component: indexErrorPage1,
    meta: {
      title: 'Error Page1 | Mofi - Premium Vue Admin Template',
      requiresAuth: true
    }
  },
  {
    path: "/error_page2",
    name: "errorPage2",
    component: indexErrorPage2,
    meta: {
      title: 'Error Page2 | Mofi - Premium Vue Admin Template',
      requiresAuth: true
    }
  },
  {
    path: "/error_page3",
    name: "errorPage3",
    component: indexErrorPage3,
    meta: {
      title: 'Error Page3 | Mofi - Premium Vue Admin Template',
      requiresAuth: true
    }
  },
  {
    path: "/error_page4",
    name: "errorPage4",
    component: indexErrorPage4,
    meta: {
      title: 'Error Page4 | Mofi - Premium Vue Admin Template',
      requiresAuth: true
    }
  },
  {
    path: "/error_page5",
    name: "errorPage5",
    component: indexErrorPage5,
    meta: {
      title: 'Error Page5 | Mofi - Premium Vue Admin Template',
      requiresAuth: true
    }
  },
  {
    path: "/error_page6",
    name: "errorPage6",
    component: indexErrorPage6,
    meta: {
      title: 'Error Page6 | Mofi - Premium Vue Admin Template',
      requiresAuth: true
    }
  },
  {
    path: "/comingsoon/comingsoon_simple",
    name: "comingsoonPage",
    component: indexComingsoonPage,
    meta: {
      title: 'Comingsoon Page | Mofi - Premium Vue Admin Template',
      requiresAuth: true
    }
  },
  {
    path: "/comingsoon/comingsoon_video",
    name: "comingsoonVideo",
    component: indexComingsoonVideo,
    meta: {
      title: 'Comingsoon Video | Mofi - Premium Vue Admin Template',
      requiresAuth: true
    }
  },
  {
    path: "/comingsoon/comingsoon_image",
    name: "comingsoonImage",
    component: indexComingsoonImage,
    meta: {
      title: 'Comingsoon Image | Mofi - Premium Vue Admin Template',
      requiresAuth: true
    }
  },
  {
    path: "/authentication/simple",
    name: "loginsimple",
    component: loginSimple,
    meta: {
      title: 'Login Simple | Mofi - Premium Vue Admin Template',
      requiresAuth: false
    }
  },
  {
    path: "/authentication/login/one",
    name: "loginimage",
    component: loginImage,
    meta: {
      title: 'Login Image | Mofi - Premium Vue Admin Template',
      requiresAuth: false
    }
  },
  {
    path: "/authentication/login/two",
    name: "loginImagetwo",
    component: loginImageTwo,
    meta: {
      title: 'Login Image Two | Mofi - Premium Vue Admin Template',
      requiresAuth: false
    }
  },
  {
    path: "/authentication/login/validate",
    name: "loginValidation",
    component: loginValidation,
    meta: {
      title: 'Login Validation | Mofi - Premium Vue Admin Template',
      requiresAuth: false
    }
  },
  {
    path: "/authentication/login/tooltip",
    name: "loginTooltip",
    component: loginTooltip,
    meta: {
      title: 'Login Tooltip | Mofi - Premium Vue Admin Template',
      requiresAuth: false
    }
  },
  {
    path: "/authentication/login/sweetalert",
    name: "loginSweetalert",
    component: loginSweetalert,
    meta: {
      title: 'Login Sweetalert | Mofi - Premium Vue Admin Template',
      requiresAuth: false
    }
  },
  {
    path: "/authentication/register/two",
    name: "registerImagetwo",
    component: registerImageTwo,
    meta: {
      title: 'Register Image Two | Mofi - Premium Vue Admin Template',
      requiresAuth: false
    }
  },
  {
    path: "/auth/register",
    name: "registerSimple",
    component: registerSimple,
    meta: {
      title: 'Register | Mofi - Premium Vue Admin Template',
      requiresAuth: false
    }
  },
  {
    path: "/authentication/register/one",
    name: "registerImage",
    component: registerImage,
    meta: {
      title: 'Register Image | Mofi - Premium Vue Admin Template',
      requiresAuth: false
    }
  },
  {
    path: "/authentication/unlock_user",
    name: "unlockUser",
    component: unlockUser,
    meta: {
      title: 'Unlock User | Mofi - Premium Vue Admin Template',
      requiresAuth: false
    }
  },
  {
    path: "/authentication/forget_password",
    name: "forgetPassword",
    component: forgetPassword,
    meta: {
      title: 'Forget Password | Mofi - Premium Vue Admin Template',
      requiresAuth: false
    }
  },
  {
    path: "/authentication/reset_password",
    name: "resetPassword",
    component: resetPassword,
    meta: {
      title: 'Reset Password | Mofi - Premium Vue Admin Template',
      requiresAuth: false
    }
  },
  {
    path: "/authentication/maintenance",
    name: "maintenanceView",
    component: maintenanceView,
    meta: {
      title: 'Maintenance | Mofi - Premium Vue Admin Template',
      requiresAuth: false
    }
  },
  {
    path: "/gallery",
    component: BodyView,
    children: [
      {
        path: "grid_gallery",
        name: "Gallerygrid",
        component: indexGallery,
        meta: {
          title: 'Grid Gallery | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "gallery_desc",
        name: "griddesc",
        component: indexGriddesc,
        meta: {
          title: 'Grid Gallery With Desc | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "gallery_masonary",
        name: "Masonry",
        component: indexMasonry,
        meta: {
          title: 'Masonry | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "gallery_masonary_desc",
        name: "Masonarydesc",
        component: indexMasonarydesc,
        meta: {
          title: 'Masonry Desc | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "hover_effect",
        name: "hovergallery",
        component: indexHoverGallery,
        meta: {
          title: 'Hover Gallery | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: "/blog",
    component: BodyView,
    children: [
      {
        path: "details",
        name: "blogdetails",
        component: indexDetails,
        meta: {
          title: 'Blog Details | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "single",
        name: "blogsingle",
        component: indexSingle,
        meta: {
          title: 'Blog Single | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "add_post",
        name: "addpost",
        component: indexAdd,
        meta: {
          title: 'Add Post | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: "/job",
    component: BodyView,
    children: [
      {
        path: "card",
        name: "jobcard",
        component: indexJobCard,
        meta: {
          title: 'Job Card | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "/job/details/:id",
        name: "jobdetails",
        component: indexJobDetails,
        props: true,
        meta: {
          title: 'Job Details | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "apply/:id",
        name: "jobapply",
        component: indexApply,
        meta: {
          title: 'Job Apply | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "list",
        name: "joblist",
        component: indexList,
        meta: {
          title: 'Job List | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: "/learning",
    component: BodyView,
    children: [
      {
        path: "list",
        name: "Learninglist",
        component: indexLearning,
        meta: {
          title: 'Learning List | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "details/:id",
        name: "coursedetailed",
        component: indexCourse,
        meta: {
          title: 'course Detailed | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: "/maps",
    component: BodyView,
    children: [
      {
        path: "vue_google_maps",
        name: "googlemaps",
        component: indexGoogleMap,
        meta: {
          title: 'Google Map | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "vue_leaflet_maps",
        name: "mapLeaflet",
        component: indexLeaflet,
        meta: {
          title: 'Leaflet Map | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },

    ]
  },
  {
    path: "/editor",
    component: BodyView,
    children: [
      {
        path: "simple_editor",
        name: "simpleEditor",
        component: simpleEditor,
        meta: {
          title: 'Simple Editor | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "ck_editor",
        name: "ckeditor",
        component: indexCk,
        meta: {
          title: 'Ck Editor | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: "/knowledgebase",
    component: BodyView,
    children: [
      {
        path: "knowledgebase",
        name: "Knowledgebase",
        component: indexKnowledgebase,
        meta: {
          title: 'Knowledgebase | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
    ]
  },
  {
    path: "/advance",
    component: BodyView,
    children: [
      {
        path: "scrollable",
        name: "Scrollable",
        component: indexScrollable,
        meta: {
          title: 'Bonus UI  Scrollable | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "tree",
        name: "tree",
        component: indexTree,
        meta: {
          title: 'Bonus UI  Tree | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "toasts",
        name: "Toasts",
        component: indexToasts,
        meta: {
          title: 'Bonus UI  Toasts | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "rating",
        name: "rating",
        component: indexRating,
        meta: {
          title: 'Bonus UI  Rating | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "dropzone",
        name: "Dropzone",
        component: indexDropzone,
        meta: {
          title: 'Bonus UI  Dropzone | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "tour",
        name: "tour",
        component: indexTour,
        meta: {
          title: 'Bonus UI  Tour | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "sweetalert",
        name: "sweetalert",
        component: indexSweetalert,
        meta: {
          title: 'Bonus UI  SweetAlert | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "animated_modal",
        name: "animationModal",
        component: animationModal,
        meta: {
          title: 'Bonus UI  Animated Modal | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "owl_carousel",
        name: "owlCarousel",
        component: owlCarousel,
        meta: {
          title: 'Bonus UI  Owl Carousel | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "ribbons",
        name: "ribbon",
        component: indexRibbon,
        meta: {
          title: 'Bonus UI  Ribbons | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "pagination",
        name: "pagenation",
        component: indexPagenation,
        meta: {
          title: 'Bonus UI  Pagenation | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "breadcrumb",
        name: "Breadcrumb",
        component: indexBreadcrumb,
        meta: {
          title: 'Bonus UI  Breadcrumb | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "range_slider",
        name: "Range",
        component: indexRange,
        meta: {
          title: 'Bonus UI  Range | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "image_cropper",
        name: "imageCropper",
        component: indexCropper,
        meta: {
          title: 'Bonus UI  imageCropper | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "basic_card",
        name: "Basiccard",
        component: indexBasiccard,
        meta: {
          title: 'Bonus UI  Basic Card | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "creative_card",
        name: "Creative",
        component: indexCreative,
        meta: {
          title: 'Bonus UI  Creative Card | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "draggable_card",
        name: "Draggable",
        component: indexDraggable,
        meta: {
          title: 'Bonus UI  Draggable Card | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      },
      {
        path: "timeline",
        name: "indexTimeline",
        component: indexTimeline,
        meta: {
          title: 'Bonus UI  Timeline | Mofi - Premium Vue Admin Template',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/users_management',
    component: BodyView,
    meta: { 
      requiresAuth: true,
      requiresAdmin: true
    },
    beforeEnter: async (to, from, next) => {
      const { checkAuth, isAdmin } = useAuth()
      await checkAuth()
      
      if (!isAdmin.value) {
        next('/dashboard/default')
      } else {
        next()
      }
    },
    children: [
      {
        path: '',
        name: 'UserManagement',
        component: () => import('@/pages/users_management/indexUserManagement.vue')
      }
    ]
  },
  {
    path: '/dashboards/Main_Dashboard',
    name: 'MainDashboard',
    component: () => import('@/pages/dashbords/indexHome.vue'),
    meta: {
      requiresAuth: true,
      title: 'Main Dashboard'
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach(async (to, from, next) => {
  const { checkAuth } = useAuth()
  
  // Allow access to login page without authentication
  if (to.path === '/auth/login') {
    const isAuthenticated = await checkAuth()
    if (isAuthenticated) {
      next('/')
      return
    }
    next()
    return
  }

  // Check authentication for protected routes
  const isAuthenticated = await checkAuth()
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/auth/login')
    return
  }
  
  next()
})

export default router

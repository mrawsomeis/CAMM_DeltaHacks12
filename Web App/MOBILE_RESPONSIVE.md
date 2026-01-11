# Mobile Responsive Design

The CAMM application is fully optimized for mobile devices with comprehensive responsive design.

## Mobile Optimizations Implemented

### 1. **Touch-Friendly Interface**
- All buttons have minimum 48px height for easy tapping
- Full-width buttons on mobile for better touch targets
- Increased padding and spacing for mobile interaction
- Disabled text selection on buttons and interactive elements

### 2. **Responsive Navigation**
- Navigation links stack vertically on mobile
- Sticky navigation bar for easy access
- Touch-friendly navigation links with proper spacing

### 3. **Mobile-Optimized Forms**
- Input fields use 16px font size to prevent iOS Safari zoom
- Full-width form inputs on mobile
- Touch-friendly select dropdowns (48px minimum height)
- Form rows stack vertically on mobile devices
- Textareas are properly sized for mobile

### 4. **Face Capture (Mobile Camera)**
- Mobile-friendly camera constraints
- Proper video element attributes (`playsinline` for iOS)
- Responsive video container with proper aspect ratio
- Touch-friendly capture buttons
- Full-width image preview on mobile

### 5. **Responsive Layouts**
- Cards and containers adjust padding for mobile
- Grid layouts become single column on mobile
- Flexible spacing and margins optimized for small screens
- Content padding adjusted for mobile readability

### 6. **Typography**
- Responsive font sizes (smaller on mobile, larger on desktop)
- Proper line heights for mobile readability
- Hero sections scale appropriately

### 7. **Page-Specific Mobile Optimizations**

**Homepage:**
- Hero section with responsive typography
- Feature cards stack vertically on mobile
- Proper spacing and padding

**Consent Page:**
- Full-width checkbox with touch-friendly size
- Button groups stack vertically
- Improved readability on small screens

**Registration Page:**
- Form fields stack in single column
- Face capture video responsive container
- Full-width buttons for form submission
- Touch-friendly capture controls

**Alerts Page:**
- Alert cards optimized for mobile viewing
- Full-width alert creation form
- Responsive alert information display
- Touch-friendly status badges

### 8. **Viewport Configuration**
- Proper viewport meta tag with mobile settings
- Mobile web app capabilities enabled
- iOS Safari optimizations included

## Breakpoints

The application uses a primary breakpoint at **768px**:
- **Desktop**: > 768px - Multi-column layouts, hover effects
- **Mobile**: ≤ 768px - Single column, touch-optimized, stacked layouts

## Testing on Mobile

To test the mobile responsiveness:

1. **Browser DevTools**: Use Chrome/Firefox DevTools device emulation
2. **Real Devices**: Test on actual iOS and Android devices
3. **Viewport Testing**: Resize browser window to < 768px width

## Mobile-Specific Features

- **Camera Access**: Works on mobile browsers with proper permissions
- **Touch Gestures**: All interactions optimized for touch
- **Orientation**: Works in both portrait and landscape modes
- **Performance**: Optimized for mobile data speeds

## Known Mobile Considerations

1. **Camera Permissions**: Users must explicitly grant camera permissions on mobile browsers
2. **iOS Safari**: Uses `playsinline` attribute to prevent fullscreen video
3. **Font Size**: Forms use 16px minimum to prevent iOS zoom on focus
4. **Touch Targets**: All interactive elements meet 48x48px minimum size

## Browser Support

Tested and optimized for:
- iOS Safari (12+)
- Chrome Mobile (Android)
- Firefox Mobile
- Samsung Internet
- Edge Mobile

import React from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import {
  AppBar,
  Box,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Menu,
  MenuItem,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Inventory as InventoryIcon,
  Receipt as ReceiptIcon,
  CloudUpload as CloudUploadIcon,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';

const Navbar = () => {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
    handleClose();
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography
          variant="h6"
          component={RouterLink}
          to="/"
          sx={{
            flexGrow: 1,
            textDecoration: 'none',
            color: 'inherit',
            display: 'flex',
            alignItems: 'center',
          }}
        >
          <InventoryIcon sx={{ mr: 1 }} />
          Smart Inventory Scanner
        </Typography>

        {isAuthenticated ? (
          <>
            <Box sx={{ display: { xs: 'none', md: 'flex' } }}>
              <Button
                color="inherit"
                component={RouterLink}
                to="/upload"
                startIcon={<CloudUploadIcon />}
              >
                Upload Bill
              </Button>
              <Button
                color="inherit"
                component={RouterLink}
                to="/inventory"
                startIcon={<InventoryIcon />}
              >
                Inventory
              </Button>
              <Button
                color="inherit"
                component={RouterLink}
                to="/bills"
                startIcon={<ReceiptIcon />}
              >
                Bills
              </Button>
              <Button color="inherit" onClick={handleLogout}>
                Logout
              </Button>
            </Box>
            <Box sx={{ display: { xs: 'flex', md: 'none' } }}>
              <IconButton
                size="large"
                edge="end"
                color="inherit"
                aria-label="menu"
                onClick={handleMenu}
              >
                <MenuIcon />
              </IconButton>
              <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleClose}
              >
                <MenuItem
                  component={RouterLink}
                  to="/upload"
                  onClick={handleClose}
                >
                  Upload Bill
                </MenuItem>
                <MenuItem
                  component={RouterLink}
                  to="/inventory"
                  onClick={handleClose}
                >
                  Inventory
                </MenuItem>
                <MenuItem
                  component={RouterLink}
                  to="/bills"
                  onClick={handleClose}
                >
                  Bills
                </MenuItem>
                <MenuItem onClick={handleLogout}>Logout</MenuItem>
              </Menu>
            </Box>
          </>
        ) : (
          <Box>
            <Button color="inherit" component={RouterLink} to="/login">
              Login
            </Button>
            <Button color="inherit" component={RouterLink} to="/register">
              Register
            </Button>
          </Box>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Navbar; 
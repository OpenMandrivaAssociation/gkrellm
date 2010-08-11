%define name        gkrellm
%define version     2.3.4
%define release     %mkrel 10
%define title       Gkrellm
%define longtitle   A GTK-based monitoring app

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Multiple stacked system monitors
License:        GPLv3+
Group:          Monitoring
URL:            http://gkrellm.net
Source0:        http://members.dslextreme.com/users/billw/gkrellm/%{name}-%{version}.tar.bz2
Source4:        gkrellm-themes.tar.bz2
Source5:        gkrellmd.init
Patch0:         gkrellm-2.3.2-wformat.patch
Patch1:         gkrellm-2.3.4-fix-link.patch
Patch2:         gkrellm-2.3.4-force-libsensor-test-result.patch
BuildRequires:  gettext
BuildRequires:  gtk+2-devel
BuildRequires:  imagemagick
BuildRequires:  openssl-devel
BuildRequires:  libsm-devel
BuildRequires:	libntlm-devel
BuildRequires:  lm_sensors-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
GKrellM charts SMP CPU, load, Disk, and all active net interfaces
automatically. An on/off button and online timer for the PPP interface
is provided. Monitors for memory and swap usage, file system, internet
connections, APM laptop battery, mbox style mailboxes, and cpu temps.
Also includes an uptime monitor, a hostname label, and a clock/calendar.
Additional features are:

  * Autoscaling grid lines with configurable grid line resolution.
  * LED indicators for the net interfaces.
  * A gui popup for configuration of chart sizes and resolutions.

%package    devel
Summary:    Include files for gkrellm
Group:      Development/Other
Requires:   %name = %version

%description    devel
gkrellm header files for gkrellm development and plugin support.

%package server
Summary:        Server component for gkrellm
Group:          Monitoring
Requires(post): rpm-helper
Requires(preun):rpm-helper

%description    server
The server component allows you to monitor a server remotely from 
a client running gkrellm, without installing gkrellm on the server.

%prep
%setup -q
%setup -q -D -T -a4
for i in `find -type d -name .xvpics`
    do rm -rf $i
done
# make it lib64 aware
perl -pi -e "/PLUGINS_DIR/ and s|/lib/|/%{_lib}/|g" ./src/gkrellm.h ./server/gkrellmd.h
perl -pi -e "s|/lib/|/%{_lib}/|" Makefile
%patch0 -p1 -b .wformat
%patch1 -p0 -b .link
%patch2 -p1 -b .libsensors

%build
%make INSTALLROOT=%{_prefix} \
      INCLUDEDIR=%{_includedir} \
      CFLAGS="%optflags" \
      LINK_FLAGS="%ldflags -Wl,-E" \
      LOCALEDIR=%{_datadir}/locale

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
make install \
    INSTALLROOT=%{buildroot}%{_prefix} \
    INSTALLDIR=%{buildroot}/%{_bindir} \
    INCLUDEDIR=%{buildroot}%{_includedir} \
    MANDIR=%{buildroot}%{_mandir}/man1 \
    LOCALEDIR=%{buildroot}%{_datadir}/locale \
    STRIP=""

mkdir -p %{buildroot}%{_libdir}/%{name}2/plugins

mkdir -p %{buildroot}{%{_iconsdir},%{_liconsdir},%{_miconsdir}}
convert src/icon.xpm -geometry 48x48 %{buildroot}%{_liconsdir}/%{name}.png
convert src/icon.xpm -geometry 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert src/icon.xpm -geometry 16x16 %{buildroot}%{_miconsdir}/%{name}.png

mkdir -p %{buildroot}%{_datadir}/%{name}2/themes
cp -av gkrellm-themes/* %{buildroot}%{_datadir}/%{name}2/themes

install -d -m 755 %{buildroot}%{_datadir}/applications
cat >  %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{title}
Comment=%{longtitle}
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=GTK;System;Monitor;
EOF

install -d -m 755 %{buildroot}%{_sysconfdir}
install -m 644 server/gkrellmd.conf %{buildroot}%{_sysconfdir}

install -d -m 755 %{buildroot}%{_initrddir}
install -m 755 %{SOURCE5} %{buildroot}%{_initrddir}/gkrellmd

%multiarch_includes %{buildroot}%{_includedir}/gkrellm2/gkrellm.h
%multiarch_includes %{buildroot}%{_includedir}/gkrellm2/gkrellmd.h

%{find_lang} %{name}

# lock dir
install -d -m 755 %{buildroot}%{_localstatedir}/lock/gkrellm
chmod 1777 %{buildroot}%{_localstatedir}/lock/gkrellm

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%update_menus
%endif
   
%if %mdkversion < 200900
%postun
%clean_menus
%endif

%post server
%_post_service gkrellmd 

%preun server
%_preun_service gkrellmd

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYRIGHT Changelog INSTALL README *.html
%{_bindir}/gkrellm
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/gkrellm.png
%{_liconsdir}/gkrellm.png
%{_miconsdir}/gkrellm.png 
%{_mandir}/man1/gkrellm.1*
%{_libdir}/gkrellm2
%{_datadir}/gkrellm2
%{_localstatedir}/lock/gkrellm

%files devel
%defattr(-,root,root)
%doc *.html
%{_includedir}/gkrellm2
%{_libdir}/pkgconfig/gkrellm.pc
%multiarch %{_includedir}/multiarch-*/gkrellm2

%files server
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/gkrellmd.conf
%{_initrddir}/gkrellmd
%{_bindir}/gkrellmd
%{_mandir}/man1/gkrellmd.1*


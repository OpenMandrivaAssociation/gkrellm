%define name    gkrellm
%define version 2.2.9
%define release %mkrel 4
%define title       Gkrellm
%define longtitle   A GTK-based monitoring app

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Multiple stacked system monitors
License:        GPL
Group:          Monitoring
URL:            http://gkrellm.net
Source0:        http://members.dslextreme.com/users/billw/gkrellm/%{name}-%{version}.tar.bz2
Source4:        gkrellm-themes.tar.bz2
Source5:        gkrellmd.init.bz2
Source6:        %{name}.bash-completion.bz2
BuildRequires:  gettext
BuildRequires:  gtk+2-devel
BuildRequires:  ImageMagick
BuildRequires:  openssl-devel
BuildRequires:  libsm-devel
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
bzcat %{SOURCE5} > %{name}.init
bzcat %{SOURCE6} > %{name}.bash-completion
for i in `find -type d -name .xvpics`
    do rm -rf $i
done
# make it lib64 aware
perl -pi -e "/PLUGINS_DIR/ and s|/lib/|/%{_lib}/|g" ./src/gkrellm.h
perl -pi -e "s|/lib/|/%{_lib}/|" Makefile

%build
%make CFLAGS="$RPM_OPT_FLAGS" \
      SMC_LIBS="-L%{_prefix}/X11R6/%{_lib} -lSM -lICE" \
      LOCALEDIR=%{_datadir}/locale

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
make install INSTALLROOT=%{buildroot}%{_prefix} INSTALLDIR=%{buildroot}/%{_bindir} \
  INCLUDEDIR=%{buildroot}%{_includedir} MANDIR=%{buildroot}%{_mandir}/man1 \
  LOCALEDIR=%{buildroot}%{_datadir}/locale

mkdir -p %{buildroot}%{_libdir}/%{name}2/plugins

mkdir -p %{buildroot}{%{_iconsdir},%{_liconsdir},%{_miconsdir}}
convert src/icon.xpm -geometry 48x48 %{buildroot}%{_liconsdir}/%{name}.png
convert src/icon.xpm -geometry 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert src/icon.xpm -geometry 16x16 %{buildroot}%{_miconsdir}/%{name}.png

mkdir -p %{buildroot}%{_datadir}/%{name}2/themes
cp -av gkrellm-themes/* %{buildroot}%{_datadir}/%{name}2/themes

mkdir -p %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/gkrellm <<EOF
?package(gkrellm): \
    command="%{_bindir}/gkrellm" \
    needs="x11" \
    section="System/Monitoring" \
    icon="%{name}.png" \
    startup_notify="true" \
    title="%{title}" \
    longtitle="%{longtitle}" \
    xdg="true" 
EOF

install -d -m 755 %{buildroot}%{_datadir}/applications
cat >  %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=%{title}
Comment=%{longtitle}
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=GTK;X-MandrivaLinux-System-Monitoring;System;Monitor;
EOF

install -d -m 755 %{buildroot}%{_sysconfdir}
install -m 644 server/gkrellmd.conf %{buildroot}%{_sysconfdir}

install -d -m 755 %{buildroot}%{_initrddir}
install -m 755 %{name}.init %{buildroot}%{_initrddir}/gkrellmd

install -d -m 755 %{buildroot}%{_sysconfdir}/bash_completion.d
install -m 644 %{name}.bash-completion %{buildroot}%{_sysconfdir}/bash_completion.d/%{name}

%multiarch_includes %{buildroot}%{_includedir}/gkrellm2/gkrellm.h
%multiarch_includes %{buildroot}%{_includedir}/gkrellm2/gkrellmd.h

%{find_lang} %{name}

%clean
rm -rf %{buildroot}

%post
%update_menus
   
%postun
%clean_menus

%post server
%_post_service gkrellmd 

%preun server
%_preun_service gkrellmd

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYRIGHT Changelog INSTALL README *.html
%config(noreplace) %{_sysconfdir}/bash_completion.d/%{name}
%{_bindir}/gkrellm
%{_menudir}/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/gkrellm.png
%{_liconsdir}/gkrellm.png
%{_miconsdir}/gkrellm.png 
%{_mandir}/man1/gkrellm.1*
%{_libdir}/gkrellm2
%{_datadir}/gkrellm2

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


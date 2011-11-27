Name:          xml-commons-apis
Version:       1.4.01
Release:       5
Summary:       APIs for DOM, SAX, and JAXP
Group:         Development/Java
License:       ASL 2.0 and W3C and Public Domain
URL:           http://xml.apache.org/commons/

# From source control because the published tarball doesn't include some docs:
#   svn export http://svn.apache.org/repos/asf/xml/commons/tags/xml-commons-external-1_4_01/java/external/
#   tar czf xml-commons-external-1.4.01-src.tar.gz external
Source0:       xml-commons-external-%{version}-src.tar.gz
Source1:       %{name}-MANIFEST.MF
Source2:       %{name}-ext-MANIFEST.MF

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:     noarch

BuildRequires: java-devel >= 0:1.6.0
BuildRequires: jpackage-utils
BuildRequires: ant
BuildRequires: zip
Requires:      java
Requires:      jpackage-utils

Obsoletes:     xml-commons < %{version}-%{release}
Provides:      xml-commons = %{version}-%{release}

# TODO: Ugh, this next line should be dropped since it actually provides JAXP 1.4 now...
Provides:      xml-commons-jaxp-1.3-apis = %{version}-%{release}

%description
xml-commons-apis is designed to organize and have common packaging for
the various externally-defined standard interfaces for XML. This
includes the DOM, SAX, and JAXP. 

%package manual
Summary:       Manual for %{name}
Group:         Development/Java

%description manual
%{summary}.

%package javadoc
Summary:       Javadoc for %{name}
Group:         Development/Java

%description javadoc
%{summary}.

%prep
%setup -q -n external

# Make sure upstream hasn't sneaked in any jars we don't know about
find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

# Fix file encodings
iconv -f iso8859-1 -t utf-8 LICENSE.dom-documentation.txt > \
  LICENSE.dom-doc.temp && mv -f LICENSE.dom-doc.temp LICENSE.dom-documentation.txt
iconv -f iso8859-1 -t utf-8 LICENSE.dom-software.txt > \
  LICENSE.dom-sof.temp && mv -f LICENSE.dom-sof.temp LICENSE.dom-software.txt

%build
ant -Dant.build.javac.source=1.5 -Dant.build.javac.target=1.5 jar javadoc

%install
rm -rf %{buildroot}

# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE1} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/xml-apis.jar META-INF/MANIFEST.MF
cp -p %{SOURCE2} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/xml-apis-ext.jar META-INF/MANIFEST.MF

# Jars
install -pD -T build/xml-apis.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
install -pD -T build/xml-apis-ext.jar %{buildroot}%{_javadir}/%{name}-ext-%{version}.jar

# Jar versioning
(cd %{buildroot}%{_javadir} && for jar in %{name}-%{version}.jar; do ln -sf ${jar} dom3-${jar}; done)
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)
# for better interoperability with the jpp apis packages
ln -sf %{name}.jar %{buildroot}%{_javadir}/jaxp13.jar
ln -sf %{name}.jar %{buildroot}%{_javadir}/jaxp.jar
ln -sf %{name}.jar %{buildroot}%{_javadir}/xml-commons-jaxp-1.3-apis.jar

# Javadocs
mkdir -p %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr build/docs/javadoc/* \
  %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name} 

# prevent apis javadoc from being included in doc
rm -rf build/docs/javadoc

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE NOTICE 
%doc LICENSE.dom-documentation.txt README.dom.txt
%doc LICENSE.dom-software.txt LICENSE.sac.html
%doc LICENSE.sax.txt README-sax  README.sax.txt
%{_javadir}/*

%files manual
%defattr(-,root,root,-)
%doc build/docs/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/*

